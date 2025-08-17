# API Documentation

## Endpoints

### POST /evaluate
Evaluate a regulatory compliance strategy.

**Request Body:**
```json
{
  "description": "Strategy description",
  "jurisdiction": "Target jurisdiction code",
  "type": "Strategy type",
  "profit_potential": 1000000,
  "implementation_cost": 100000,
  "time_horizon_months": 24
}
```

**Response:**
```json
{
  "success": true,
  "strategy_id": "uuid",
  "expected_value": 500000,
  "decision": "EXECUTE|CAUTION|AVOID",
  "confidence_score": 0.75,
  "risk_zone": "GREEN|YELLOW|RED"
}
```

### GET /transparency
View aggregated compliance evaluation data.

### GET /regulatory-insights
Get insights for regulatory bodies.

### GET /market-trends
View current market trends and conditions.

### GET /health
Health check endpoint.