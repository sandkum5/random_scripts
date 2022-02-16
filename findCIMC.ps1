# This script connects to the provided IP's and makes a Redfish API call and prints the CIMC product,vendor Info.
# Need to add Error checks

$subnet   = Read-Host "Please enter the subnet id in format [198.19.216]: "
$start_ip = Read-Host "Please enter the start IP last octet [163]: "
$end_ip   = Read-Host "Please enter the end IP last octet [167]: "

$start_ip..$end_ip | ForEach-Object {
    $targetIp = "$subnet.$_"
    $response = ""
    $uri = "https://$targetIp/redfish/v1"
    try {
        if (Test-Connection -TargetName $targetIp -Quiet -Count 2 -Delay 1) {
            $response = Invoke-WebRequest -SkipCertificateCheck -Method 'GET' -Uri $uri -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                $responseStatusCode = $response.StatusCode
                $product = ($response.Content | ConvertFrom-Json).Product
                $vendor = ($response.Content | ConvertFrom-Json).Vendor
                Write-Host "Target: $targetIp, Product Id: $product, Company: $vendor"
            }
            else {
                Write-Host "Response Status Code: $response.StatusCode"
                Write-Host "Not a Cisco UCS Server"
            }
        } else {
            Write-Host "Target: $targetIp, Not Reachable"
        }
    } catch {
        Write-Host $_.Exception.Response.StatusDescription
        Write-Host $_.Exception.Response.StatusCode.Value__
    }
}
