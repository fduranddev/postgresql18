Set-StrictMode -Version Latest

$PSModule = $ExecutionContext.SessionState.Module
$PSModuleRoot = $PSModule.ModuleBase

$binaryModuleManifestFile = 'PostgreSQLCmdlets.psd1'
$binaryModuleRootPath = $PSModuleRoot
$binaryModuleRootPath = Join-Path -Path $PSModuleRoot -ChildPath 'lib/netstandard2.1'
$binaryModulePath = Join-Path -Path $binaryModuleRootPath -ChildPath $binaryModuleManifestFile
$binaryModule = Import-Module -Name $binaryModulePath -PassThru

$PSModule.OnRemove = {
  Remove-Module -ModuleInfo $binaryModule
}