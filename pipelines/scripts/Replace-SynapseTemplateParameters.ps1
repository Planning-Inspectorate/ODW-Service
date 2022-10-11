[CmdletBinding()]
Param(
  [Parameter(Mandatory=$false)]
  [String]$TemplateParameterFilePath = (Get-Location).Path,

  [Parameter(Mandatory=$false)]
  [String]$TemplateParameterFileName = "TemplateParametersForWorkspace.json",

  [Parameter(Mandatory=$false)]
  [Hashtable]$Overrides = @{},

  [Parameter(Mandatory=$false)]
  [String]$OverrideParameterFileName = "TemplateParameterOverridesForWorkspace.json"
)

# Determine parameters and values for override
$ParametersFile = Get-Content "$TemplateParameterFilePath/$TemplateParameterFileName" | ConvertFrom-Json
$Parameters     = $ParametersFile.parameters
$ParameterNames = ($Parameters | Get-Member | Where-Object { $_.MemberType -eq 'NoteProperty' }).Name
$ParameterList  = [System.Collections.Generic.List[PsCustomObject]]::new()
Foreach ($P in $ParameterNames) {
  $ParameterList += [PsCustomObject]@{
    Name  = $P
    Value = $Parameters.$P.Value
  }
}

# Find and replace parameter values
$ParameterOverridesHash = @{}
Foreach ($K in $Overrides.GetEnumerator()) {
  $F = $K.Name
  $R = $K.Value
  Foreach ($P in $ParameterList) {
    Write-Host "$($P.Name): " -NoNewLine
    If ($P.Value -like "*$($F)*") {
      Write-Host "Overriding $($P.Value) with $($P.Value.Replace($F,$R))"
      $ParameterOverridesHash[$P.Name] = [PsCustomObject]@{
        value = $P.Value.Replace($F,$R)
      }
    } Else {
      Write-Host "No override required"
      $ParameterOverridesHash[$P.Name] = [PsCustomObject]@{
        value = $P.Value
      }
    }
  }
}

# Reconstruct template parameter file
$ParametersOverridesFile = [PSCustomObject]@{
  '$schema'      = $ParametersFile.'$schema'
  contentVersion = $ParametersFile.contentVersion
  parameters     = $ParameterOverridesHash
} | ConvertTo-Json -Depth 10

# Save template parameter override file
$ParametersOverridesFile | Out-File -FilePath "$TemplateParameterFilePath/$OverrideParameterFileName"
