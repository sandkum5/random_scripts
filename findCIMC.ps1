# This script connects to the provided IP's and makes a Redfish API call and prints the CIMC product,vendor Info.
# Need to add Error checks

$subnet   = Read-Host "Please enter the subnet id in format x.y.z: [198.19.216]"
$start_ip = Read-Host "Please enter the start IP last octet: [163]"
$end_ip   = Read-Host "Please enter the end IP last octet: [167]"

$start_ip..$end_ip | ForEach-Object {
    $targetIp = "$subnet.$_"
    Write-Host "Checking Target: $targetIp"
    Write-Host "-------------------------------"
    Write-Host " "
    $response = ""
    $uri = "https://$targetIp/redfish/v1"
    $response = Invoke-RestMethod -SkipCertificateCheck -Method 'GET' -Uri $uri -TimeoutSec 2 | select Product,Vendor
    Write-Host $response | ConvertTo-Json
    Write-Host " "
}
