<#
.SYNOPSIS
    Exports lab DLP policies, rules and custom SITs to sanitised JSON with SHA-256 hashes.

.DESCRIPTION
    Read-only. Used for audit evidence (configuration at time of test) and drift detection
    (compare two exports). Only objects whose name starts with -IdPrefix are exported.
    Identity, tenant and object identifiers are removed; email addresses and GUIDs are
    replaced unless -KeepGuids is set.

    Output goes to evidence/config-export/<UTC timestamp>/ which is git-ignored. Review the
    output before committing any extract.

    STATUS: syntax-checked, NOT lab-validated.

.EXAMPLE
    ./Export-DlpConfiguration.ps1

.EXAMPLE
    ./Export-DlpConfiguration.ps1 -IdPrefix 'PV-POL-001' -OutputRoot ./evidence/config-export
#>
[CmdletBinding()]
param(
    [string]$OutputRoot = [System.IO.Path]::Combine($PSScriptRoot, '..', '..', '..', 'evidence', 'config-export'),
    [string]$IdPrefix = 'PV-',
    [switch]$KeepGuids
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command -Name Get-DlpCompliancePolicy -ErrorAction SilentlyContinue)) {
    throw 'Security & Compliance cmdlets not available. Run Connect-IPPSSession against the LAB tenant first.'
}

$stripped = @(
    'Identity', 'DistinguishedName', 'Guid', 'Id', 'ObjectId', 'ExchangeObjectId', 'OrganizationId',
    'ImmutableId', 'LastModifiedBy', 'CreatedBy', 'ModifiedBy', 'OriginatingServer', 'ExchangeVersion',
    'ObjectState', 'IsValid', 'PSComputerName', 'RunspaceId', 'PSShowComputerName'
)

function ConvertTo-SanitisedObject {
    param([Parameter(Mandatory, ValueFromPipeline)] $InputObject)
    process {
        $clean = [ordered]@{}
        foreach ($property in $InputObject.PSObject.Properties) {
            if ($stripped -notcontains $property.Name) {
                $value = $property.Value
                if ($null -ne $value -and $value -isnot [string] -and $value -is [System.Collections.IEnumerable]) {
                    $value = @($value | ForEach-Object { "$_" })
                }
                $clean[$property.Name] = $value
            }
        }
        [pscustomobject]$clean
    }
}

function Write-SanitisedJson {
    param([Parameter(Mandatory)] $Data, [Parameter(Mandatory)] [string]$Path)
    $json = $Data | ConvertTo-Json -Depth 8
    $json = [regex]::Replace($json, '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', 'user@redacted.example')
    $json = [regex]::Replace($json, '[A-Za-z0-9-]+\.onmicrosoft\.com', 'redacted.example')
    if (-not $KeepGuids) {
        $json = [regex]::Replace($json, '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', '00000000-0000-0000-0000-000000000000')
    }
    Set-Content -Path $Path -Value $json -Encoding utf8
}

$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$outDir = [System.IO.Path]::Combine($OutputRoot, $stamp)
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$policies = @(Get-DlpCompliancePolicy | Where-Object { $_.Name -like "$IdPrefix*" })
$policyNames = $policies.Name
$rules = @(Get-DlpComplianceRule | Where-Object { $policyNames -contains $_.ParentPolicyName })
$customSits = @(Get-DlpSensitiveInformationType | Where-Object { $_.Publisher -ne 'Microsoft Corporation' })

Write-SanitisedJson -Data @($policies | ConvertTo-SanitisedObject) -Path (Join-Path $outDir 'policies.json')
Write-SanitisedJson -Data @($rules | ConvertTo-SanitisedObject) -Path (Join-Path $outDir 'rules.json')
Write-SanitisedJson -Data @($customSits | ConvertTo-SanitisedObject) -Path (Join-Path $outDir 'custom-sits.json')

$manifest = Get-ChildItem -Path $outDir -Filter '*.json' | ForEach-Object {
    [pscustomobject]@{
        file        = $_.Name
        sha256      = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        exported_at = $stamp
        id_prefix   = $IdPrefix
    }
}
$manifest | ConvertTo-Json | Set-Content -Path (Join-Path $outDir 'manifest.json') -Encoding utf8

Write-Output ("Exported {0} policies, {1} rules, {2} custom SITs to {3}" -f $policies.Count, $rules.Count, $customSits.Count, $outDir)
Write-Output 'Review the files before committing any extract. Raw exports stay in evidence/ (git-ignored).'
