# Savannah E-commerce API

A robust Django REST Framework API for an e-commerce platform featuring hierarchical product categories, order management, and automated notifications. Built with enterprise-grade security, containerization, and CI/CD integration.

## Features

- **Authentication & Authorization**
  - JWT-based authentication
  - Token-based API access
  - Role-based permissions
  - Comprehensive security controls

- **Product Management**
  - Hierarchical category structure (unlimited depth)
  - Full CRUD operations for products
  - Category-based product organization
  - Price tracking and updates

- **Customer Management**
  - Customer profiles with contact information
  - Order history tracking
  - Address management

- **Order Processing**
  - Order creation and management
  - Multiple products per order
  - Order status tracking
  - Automated notifications

- **Notifications**
  - SMS notifications via Africa's Talking
  - Email notifications for administrators
  - Order status updates

## Technical Stack

- Django 4.x
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Africa's Talking SMS Gateway
- Docker & Docker Compose
- Kubernetes
- GitLab CI/CD

## API Documentation

Our API is fully documented using OpenAPI (Swagger) specification. Access the interactive documentation at:

```
http://your-domain/api/docs/
```

The documentation includes:
- Detailed endpoint descriptions
- Request/response examples
- Authentication requirements
- Schema definitions

## Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- Token expiration and refresh mechanisms
- API rate limiting

### Data Security
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration
- Secure password hashing

### Error Handling
- Structured error responses
- Detailed logging
- Custom exception handling
- Graceful failure recovery

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/BenjaminKakai/E-commerce-API.git
cd savannah-ecommerce
```

2. Set up the environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the PostgreSQL database:
```bash
# Create database
createdb savannah_ecommerce

# Run migrations
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. For production deployment:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Kubernetes Deployment

1. Apply Kubernetes configurations:
```bash
kubectl apply -f k8s/
```

2. Verify deployment:
```bash
kubectl get pods
kubectl get services
```

## Testing and Quality Assurance

### Running Tests
```bash
# Run test suite
python manage.py test

# Generate coverage report
coverage run manage.py test
coverage report
coverage html  # Generates detailed HTML report
```

### Code Quality
- Linting: `flake8`
- Type checking: `mypy`
- Code formatting: `black`

## CI/CD Pipeline

Our GitLab CI/CD pipeline includes:

1. Build Stage:
   - Code linting
   - Type checking
   - Unit tests
   - Coverage reporting

2. Test Stage:
   - Integration tests
   - Security scanning
   - Performance testing

3. Deploy Stage:
   - Docker image building
   - Container scanning
   - Kubernetes deployment

## Monitoring and Logging

- Application monitoring via Prometheus
- Log aggregation with ELK stack
- Performance metrics collection
- Error tracking and alerting

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure your PR adheres to:
- Test coverage requirements
- Code style guidelines
- Documentation standards

## License

This project is licensed under the MIT License - see the LICENSE file for details.
