<#
.SYNOPSIS
    Creates PV-POL-001 (external email, bank account data) in a LAB tenant.

.DESCRIPTION
    Implements platforms/microsoft-purview/policies/PV-POL-001.yaml as three rules:
      R1  1 to (BlockThreshold-1) IBANs  -> audit + policy tip, severity Low, NO alert mail
      R2  BlockThreshold to (StrictThreshold-1) -> block with justification, alert mail, Medium
      R3  StrictThreshold or more -> block, alert mail, High
    Defaults to simulation mode (TestWithoutNotifications). Supports -WhatIf.

    Only R2 and R3 generate an alert mail, sent to -AlertRecipient. R1 is audit only.

    STATUS: detection and R1/R2/R3 routing by count were observed in the v0.3 lab campaign
    (see testing/test-matrix.csv). The block action was NOT validated, because simulation mode
    does not enforce BlockAccess. Re-check parameter behaviour against current Security &
    Compliance PowerShell documentation before any use outside a lab.

    Requires an existing session to a LAB tenant: Connect-IPPSSession. Never run against an
    employer or client tenant.

.EXAMPLE
    ./New-LabDlpPolicy.ps1 -AlertRecipient admin@lab.example -WhatIf

.EXAMPLE
    ./New-LabDlpPolicy.ps1 -AlertRecipient admin@lab.example -Mode TestWithNotifications -BlockThreshold 5 -StrictThreshold 20
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet('TestWithoutNotifications', 'TestWithNotifications', 'Enable')]
    [string]$Mode = 'TestWithoutNotifications',

    [ValidateRange(2, 100)]
    [int]$BlockThreshold = 5,

    [ValidateRange(3, 500)]
    [int]$StrictThreshold = 20,

    [Parameter(Mandatory)]
    [ValidatePattern('^[^@\s]+@[^@\s]+\.[^@\s]+$')]
    [string]$AlertRecipient,

    [string]$PolicyName = 'PV-POL-001 External email - bank account data'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($StrictThreshold -le $BlockThreshold) {
    throw 'StrictThreshold must be greater than BlockThreshold.'
}
if (-not (Get-Command -Name Get-DlpCompliancePolicy -ErrorAction SilentlyContinue)) {
    throw 'Security & Compliance cmdlets not available. Run Connect-IPPSSession against the LAB tenant first.'
}

function New-IbanCondition {
    param(
        [Parameter(Mandatory)] [int]$Min,
        [int]$Max = 0
    )
    $condition = @{
        Name            = 'International banking account number (IBAN)'
        minCount        = "$Min"
        confidencelevel = 'High'
    }
    if ($Max -gt 0) { $condition['maxCount'] = "$Max" }
    return , @($condition)
}

$existing = Get-DlpCompliancePolicy -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq $PolicyName }
if ($existing) {
    throw "Policy '$PolicyName' already exists. Remove it first or use another -PolicyName."
}

$tipText = 'LAB: this message contains client account data. External sending of client data is restricted. See the data handling guideline.'

$rules = @(
    @{ Name = 'PV-POL-001-R1 Low volume notify'; Min = 1; Max = $BlockThreshold - 1
       Block = $false; Override = $false; Severity = 'Low'; Alert = $false },
    @{ Name = 'PV-POL-001-R2 Block with justification'; Min = $BlockThreshold; Max = $StrictThreshold - 1
       Block = $true; Override = $true; Severity = 'Medium'; Alert = $true },
    @{ Name = 'PV-POL-001-R3 Strict block'; Min = $StrictThreshold; Max = 0
       Block = $true; Override = $false; Severity = 'High'; Alert = $true }
)

if ($PSCmdlet.ShouldProcess($PolicyName, "Create DLP policy (Exchange, mode $Mode)")) {
    New-DlpCompliancePolicy -Name $PolicyName `
        -ExchangeLocation All `
        -Mode $Mode `
        -Comment 'banking-dlp-controls-lab | UC-001 | spec policies/PV-POL-001.yaml' | Out-Null
}

$created = 0
foreach ($rule in $rules) {
    $params = @{
        Name                                = $rule.Name
        Policy                              = $PolicyName
        ContentContainsSensitiveInformation = (New-IbanCondition -Min $rule.Min -Max $rule.Max)
        AccessScope                         = 'NotInOrganization'
        ReportSeverityLevel                 = $rule.Severity
        NotifyUser                          = 'LastModifier'
        NotifyPolicyTipCustomText           = $tipText
    }
    if ($rule.Block) {
        $params['BlockAccess'] = $true
        if ($rule.Override) { $params['NotifyAllowOverride'] = 'WithJustification' }
    }
    if ($rule.Alert) { $params['GenerateAlert'] = @($AlertRecipient) }

    if ($PSCmdlet.ShouldProcess($rule.Name, 'Create DLP rule')) {
        try {
            New-DlpComplianceRule @params | Out-Null
            $created++
        }
        catch {
            Write-Error ("Rule '{0}' failed: {1}. The policy '{2}' exists with {3} of {4} rules. Fix the cause, then remove the policy (Remove-DlpCompliancePolicy) and rerun." -f $rule.Name, $_.Exception.Message, $PolicyName, $created, $rules.Count)
            throw
        }
    }
}

if ($WhatIfPreference) {
    Write-Output 'WhatIf: nothing was created.'
    return
}
if ($created -ne $rules.Count) {
    throw "Only $created of $($rules.Count) rules were created."
}

Write-Output "Done. Policy '$PolicyName' in mode $Mode with $created rules. Allow time for policy distribution before running TC-001 to TC-003."
Write-Output 'Next: run Export-DlpConfiguration.ps1 to capture the configuration as evidence.'
