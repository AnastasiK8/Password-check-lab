variable "image_name" {
  description = "Повна назва Docker-образу з тегом (наприклад, ghcr.io/<логін>/ci-lab-app:latest)"
  type        = string
  default     = "ghcr.io/anastasik8/ci-lab-app:latest"
}