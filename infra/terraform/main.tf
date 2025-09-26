terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC simplificada
resource "aws_vpc" "convoca" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "convocafinder-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.convoca.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.region}a"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.convoca.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.convoca.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security group para ECS/EC2
resource "aws_security_group" "app_sg" {
  name        = "convocafinder-sg"
  description = "Permite HTTP/HTTPS"
  vpc_id      = aws_vpc.convoca.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS PostgreSQL
resource "aws_db_subnet_group" "convoca" {
  name       = "convocafinder-db"
  subnet_ids = [aws_subnet.public.id]
}

resource "aws_db_instance" "postgres" {
  identifier              = "convocafinder-db"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.convoca.name
  skip_final_snapshot     = true
  publicly_accessible     = true # Para MVP, considerar privado en prod
  vpc_security_group_ids  = [aws_security_group.app_sg.id]
  deletion_protection     = false
  backup_retention_period = 7
}

# Bucket para logs
resource "aws_s3_bucket" "logs" {
  bucket = "convocafinder-logs-${var.environment}"
}

# ECS Cluster + tarea (comentado para referencia)
# resource "aws_ecs_cluster" "convoca" {
#   name = "convocafinder"
# }

# resource "aws_ecs_task_definition" "backend" {
#   family                   = "convocafinder-backend"
#   requires_compatibilities = ["FARGATE"]
#   network_mode             = "awsvpc"
#   cpu                      = "512"
#   memory                   = "1024"
#   execution_role_arn       = var.ecs_execution_role
#   container_definitions    = file("container-definitions/backend.json")
# }

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "environment" {
  type    = string
  default = "staging"
}
