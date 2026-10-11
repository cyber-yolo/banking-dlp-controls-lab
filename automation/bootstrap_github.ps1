<#
.SYNOPSIS
    Creates labels, milestones and issues from backlog/initial-backlog.csv using the GitHub CLI (gh).
    PowerShell equivalent of automation/bootstrap_github.py, for environments without Python.

.DESCRIPTION
    Dry run by default (prints the gh commands). Add -Apply to execute.
    Run once on a repository with no custom issues so numbering stays clean.
    Existing labels are updated (--force), existing milestones and issues (same title) are skipped.

.EXAMPLE
    .\bootstrap_github.ps1 -Repo cyber-yolo/banking-dlp-controls-lab
    .\bootstrap_github.ps1 -Repo cyber-yolo/banking-dlp-controls-lab -Apply
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [switch]$Apply
)

$ErrorActionPreference = "Stop"

# Resolve repo root from this script location (script lives in automation/)
$RepoRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $RepoRoot "backlog\initial-backlog.csv"))) {
    # Fallback: assume current directory is the repo root
    $RepoRoot = (Get-Location).Path
}
$BacklogPath = Join-Path $RepoRoot "backlog\initial-backlog.csv"
if (-not (Test-Path $BacklogPath)) {
    throw "Cannot find backlog\initial-backlog.csv. Run this from the repo, or place the script in automation\."
}

function Invoke-Gh {
    param([string[]]$GhArgs)
    $prefix = if ($Apply) { "RUN  " } else { "DRY  " }
    Write-Host ($prefix + "gh " + ($GhArgs -join " "))
    if ($Apply) {
        & gh @GhArgs
        if ($LASTEXITCODE -ne 0) { throw "gh exited with code $LASTEXITCODE" }
    }
}

# --- Labels (mirrors .github/labels.yml) ---
$labels = @(
    @{ name = "type/use-case";      color = "1d76db"; description = "Use case definition or change" },
    @{ name = "type/policy";        color = "0e8a16"; description = "Vendor policy specification or config" },
    @{ name = "type/test";          color = "fbca04"; description = "Test case, test data or test run" },
    @{ name = "type/governance";    color = "5319e7"; description = "Lifecycle, RACI, exceptions, KPI/KRI" },
    @{ name = "type/regulatory";    color = "b60205"; description = "Regulatory mapping" },
    @{ name = "type/automation";    color = "006b75"; description = "Scripts, CI, generator" },
    @{ name = "type/docs";          color = "c5def5"; description = "Documentation" },
    @{ name = "platform/agnostic";  color = "bfdadc"; description = "Vendor-independent layer" },
    @{ name = "platform/purview";   color = "0052cc"; description = "Microsoft Purview" },
    @{ name = "platform/symantec";  color = "d93f0b"; description = "Symantec DLP" },
    @{ name = "priority/P1";        color = "b60205"; description = "Blocking for the milestone" },
    @{ name = "priority/P2";        color = "d93f0b"; description = "Important" },
    @{ name = "priority/P3";        color = "fef2c0"; description = "Nice to have" },
    @{ name = "needs-lab";          color = "e99695"; description = "Requires a lab tenant or device" },
    @{ name = "security";           color = "000000"; description = "Repository security" },
    @{ name = "dependencies";       color = "ededed"; description = "Dependency updates" }
)

foreach ($l in $labels) {
    Invoke-Gh @("label", "create", $l.name, "--repo", $Repo, "--color", $l.color, "--description", $l.description, "--force")
}

# --- Read backlog ---
$backlog = Import-Csv -Path $BacklogPath | Sort-Object { [int]$_.id }

# --- Milestones ---
$haveMilestones = @()
if ($Apply) {
    $msJson = & gh api "repos/$Repo/milestones?state=all&per_page=100"
    if ($LASTEXITCODE -ne 0) { throw "gh api milestones failed" }
    $haveMilestones = ($msJson | ConvertFrom-Json) | ForEach-Object { $_.title }
}

$milestones = $backlog | ForEach-Object { $_.milestone } | Select-Object -Unique |
    Sort-Object { $v = $_.Substring(1).Split("."); [int]$v[0] * 100 + [int]$v[1] }

foreach ($m in $milestones) {
    if ($haveMilestones -contains $m) {
        Write-Host "SKIP existing milestone: $m"
        continue
    }
    Invoke-Gh @("api", "repos/$Repo/milestones", "-f", "title=$m")
}

# --- Issues ---
$haveIssues = @()
if ($Apply) {
    $isJson = & gh issue list --repo $Repo --state all --limit 1000 --json title
    if ($LASTEXITCODE -ne 0) { throw "gh issue list failed" }
    $haveIssues = ($isJson | ConvertFrom-Json) | ForEach-Object { $_.title }
}

foreach ($row in $backlog) {
    if ($haveIssues -contains $row.title) {
        Write-Host "SKIP existing issue: $($row.title)"
        continue
    }

    # Build depends-on string
    $deps = ($row.depends_on -split ";" | Where-Object { $_ } | ForEach-Object {
        if ($_ -match '^\d+$') { "#$_" } else { $_ }
    }) -join ", "
    if (-not $deps) { $deps = "none" }

    $body = @"
$($row.description)

**Acceptance criteria**

$($row.acceptance_criteria)

**Depends on:** $deps

_Backlog item $($row.id) (backlog/initial-backlog.csv). Synthetic data only._
"@

    $ghArgs = @("issue", "create", "--repo", $Repo, "--title", $row.title, "--body", $body, "--milestone", $row.milestone)

    foreach ($lab in ($row.labels -split ";" | Where-Object { $_ })) {
        $ghArgs += @("--label", $lab)
    }

    $prio = if ($row.priority -like "priority/*") { $row.priority } else { "priority/$($row.priority)" }
    $ghArgs += @("--label", $prio)

    Invoke-Gh $ghArgs
}

Write-Host ""
if ($Apply) {
    Write-Host "Done. Labels, milestones and issues created on $Repo."
} else {
    Write-Host "Dry run complete. Re-run with -Apply to execute."
}
