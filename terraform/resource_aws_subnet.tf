resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true  # ❌ This causes public IPs to be assigned by default
  availability_zone       = "us-west-2a"
  tags = {
    Name = "Public Subnet"
  }
}
