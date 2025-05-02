resource "aws_s3_bucket" "public_bucket" {
  bucket = "forticnapp-demo-bucket"
  acl    = "public-read"
}
