<#
.Synopsis
  This script transfers a file between a local machine and a S3 bucket with e-mail notification.
.Description
  This script transfers a file between a local machine and a S3 bucket with e-mail notification.
  This script communicates with a REST API to get a presignd URL to the S3 bucket allowing
  a download or an upload. This process is entirely tranparent. The stack behind the RESTf API
  can send email notifications of each upload or download operation so that the process
  stakeholder know when a modification has been made.  
.Parameter S3Bucket
  The name of the S3bucket.
.Parameter File
  The full path to the local file.
.Parameter S3Key
  The S3 key including any prefixes. This is a mandatory input for downloads.
  If omitted for uploads, the UTC date-time is appended to the leaf of the file.
.Parameter Upload
  Specify this switch to indicate an upload to S3. Omit this for downlod from S3.
.Parameter WhatIf
  Specify this switch to simulate the commands. Notification e-mail is still sent.
.Inputs
  string S3Bucket
  string File
  string S3Key
  switch Upload
  switch WhatIf
.Outputs
  List of operations being performed.
  - Indirectly, e-mail notification, if backend stack is configured.
.Example
  Transfer-File.ps1 -S3Bucket mybucket.com -File "c:\temp\my file.zip" -Upload
  `my file.zip` is uploaded to the `mybucket.com`, with the UTC data-time prefix.
  S3 key created (example): `20210118T1615202293Z/my file.zip`
  Append -WhatIf to simulate the command. Notification e-mail is still sent.
.Example
  Transfer-File.ps1 -S3Bucket mybucket.com -File "/Resources/my shared files.zip" -S3key "Resources/my shared files.zip" -Upload
  `my file.zip` is uploaded to the `mybucket.com`, as specified by the -S3key.
  S3 key created (example): `Resources/my shared files.zip`
  Append -WhatIf to simulate the command. Notification e-mail is still sent.
.Example
  Transfer-File.ps1 -S3Bucket mybucket.com -S3key "20210118T1615202293Z/my file.zip" -File "c:\my downloads\My File.zip"
  `20210118T1615202293Z/my file.zip` is downloaded from the `mybucket.com` to `c:\my downloads\My File.zip`
  Append -WhatIf to simulate the command. Notification e-mail is still sent.
.Notes
  The upload and download operations will show success/progress.
  Provided it is implemented in the backend, the email notification should contain:
  - a subject line: <Exception | Error | Info>/<Cost Center: value>/<AWS Region>/<Name of Lambda Function>
  - a body containing the following JSON (shown as an example):
    {
      "context":
      {
        "Bucket": "mybucket.com",
        "Function": "Name of Lambda Function",
        "Key": "Resources/my shared files.zip",
        "RequestedOperation": "write | read"
      },
      "message": "API message",
      "type": "Exception | Error | Info",
      "code": 502 | 500 | 400 | 200
    }
.Functionality
  S3 PreSigned URL
  REST API
#>

#Transfer-File.ps1
#DanielEIlie
#Created: 12/01/2021
#Updated: 18/01/2021

#Parameters
param (
  [Parameter(Mandatory=$true)]
  [String] $S3Bucket,

  [Parameter(Mandatory=$true)]
  [String] $File,

  [Parameter(Mandatory=$false)]
  [String] $S3Key,

  [Parameter(Mandatory=$false)]
  [switch] $Upload = $false,

  [Parameter(Mandatory=$false)]
  [switch] $WhatIf = $false
)

#Variables
if ($Upload) {
  $oper = "write"
  Write-Output("Uploading mode")
  if (0 -eq $S3Key.Length) { # prefix the file with the date only.
                             # strip the path to the file to retain the leaf only.
    $operationDate = Get-Date -Format FileDateTimeUniversal
    $leaf = Split-Path -Path $File -Leaf
    $S3Key = $operationDate + "/" + $leaf
  }
}else{
  $oper = "read"
  Write-Output("Downloading mode")
  if (0 -eq $S3Key.Length) {
    Write-Output("S3key must be specified for downloads.")
    exit 2
  }
}

Write-Output("The following S3 key will be used:")
Write-Output($S3Key)

Write-Output("Composing query...")
#Edit the following line
$uri = "https://<REST-API-Id>.execute-api.<AWS Region>.amazonaws.com/<Deployment stage>/access"
$query = "?bucket=" + $S3Bucket + "&operation=" + $oper + "&key=" + $S3Key
$uriComplete = $uri + $query

Write-Output("Invoking REST API...")
$restResult = Invoke-RestMethod -Uri $uriComplete -Method Get
if (200 -eq $restResult.code) {
  Write-Output("Received PreSigned URL.")
  $preSignedUrl = $restResult.preSignedUrl

  if ($WhatIf){
    Write-Output($preSignedUrl)
    Write-Output("No content was transferred.")
    Write-Output("Invoke the cmdlet again without the -WhatIf switch.")
  }else{

    Write-Output("Invoking the PreSigned URL...")
    if ($Upload) {
      # Can be done using Invoke-RestMethod:
      # Invoke-RestMethod -Uri $preSignedUrl -Method Put `
      # -InFile $File -Verbose
      # Can be done using Invoke-WebRequest (this is more like curl):
      $fileOper = Invoke-WebRequest -Uri $preSignedUrl -Method Put `
      -InFile $File
    }else{
      # Can be done using Invoke-RestMethod:
      # Invoke-RestMethod -Uri $preSignedUrl -Method Get `
      # -OutFile $File -Verbose
      $fileOper = Invoke-WebRequest -Uri $preSignedUrl -Method Get `
      -OutFile $File
    }
    Write-Output("Operation result:")
    Write-Output($fileOper | Format-List -Property StatusCode,StatusDescription)
    Write-Output("Done.")
  }
}else{
  Write-Output("Error: PreSigned URL was not generated:")
  Write-Output($restResult)
  exit 1
}
