# data_analytics_carmarket

## Technical Data Description

The dataset comprises vehicle listings with automotive sales data, containing structured records of marketplace offerings. Key attributes include:

### Metadata Fields
- `ListingID`: Unique alphanumeric identifier for each listing (primary key)
- `ListingTitle`: Unstructured text field containing seller-generated listing header
- `ListingDate`: ISO 8601 formatted timestamp of listing publication (YYYY-MM-DD HH:MM:SS)

### Geospatial Attributes
- `City`: Municipal location of vehicle (nominal categorical)
- `District`: Administrative subdivision 

### Vehicle Specifications
- `Brand`: Manufacturer name (nominal categorical)
- `Series`: Vehicle line designation (e.g., F-series, Golf)
- `Model`: Specific model variant (string)
- `Year`: Model year (ordinal integer, 1900-2025)
- `CountryOfProduction`: ISO country code of manufacturing origin

### Technical Parameters
- `EngineSize(cc)`: Displacement volume in cubic centimeters (continuous numerical)
- `EnginePower(HP)`: Rated power output in horsepower (continuous numerical)
- `TransmissionType`: Categorical (Automatic|Manual|CVT|DCT)
- `DriveTrain`: Drivetrain configuration (FWD|RWD|AWD|4WD)
- `FuelType`: Propulsion system (Gasoline|Diesel|Hybrid|BEV|PHEV)
- `BodyType`: Vehicle architecture (Sedan|SUV|Coupe|Hatchback)
- `DoorsType`: Count of access points (discrete numerical 2-5)
- `SeatType`: Number of seats including driver
- `RefuelingVolume`: Fuel tank capacity

### Operational Metrics
- `Mileage(km)`: Odometer reading in kilometers (non-negative continuous)
- `MaintenanceType`: Service history classification
- `VehicleTax`: Annual taxation cost (conditional on jurisdiction)

### Commercial Attributes
- `Price`: Listing price in local currency (positive continuous)
- `SellerType`: Vendor classification (Dealer|Private|Franchise)

### Supplementary Fields
- `Color`: Exterior color designation (hex values where available)
- `Link`: URL to source listing (URI format)

## Data Quality Considerations

### Missing Data Patterns
- Mechanical specifications (engine parameters) may show systematic nulls for electric vehicles
- Geographic fields potentially sparse in private seller listings
- Older vehicles (pre-2000) frequently lack digital maintenance records

### Value Constraints
- `Year`: Bounded 1900 ≤ x ≤ current_year+1 (anticipating new models)
- `Mileage`: Non-negative with upper bound ~1,000,000 km
- `Price`: Strictly positive 

### Temporal Consistency
- `ListingDate` should precede data collection timestamp
- Model year should be ≤ listing year + 1

### Categorical Cardinality
- High dimensionality in `Model` field (1000+ unique values)
- `Color` field requires standardization 

## Feature Engineering Opportunities

### Derived Temporal Features
- Vehicle age = `ListingDate.year` - `Year`
- Market seasonality from `ListingDate.month`

### Technical Ratios
- Power-to-weight ratio (HP/kg)
- Price-per-HP metric

### Geospatial Enrichment
- Regional price indices by City/District
- Proximity to dealership networks

### Text Mining
- Keyword extraction from `ListingTitle`
- Sentiment analysis of description text

## Statistical Expectations

### Distributions
- Right-skewed price distribution (log-transform recommended)
- Bimodal mileage distribution (new vs used vehicles)
- Multimodal year distribution (model refresh cycles)

### Anomaly Detection
- Zero-mileage used vehicles
- Extreme power-to-displacement ratios
- Mismatched drivetrain/body type combinations

### Market Segmentation
- Price clustering by brand tier
- Geographic variation in fuel type prevalence
- Seller type distribution across price quartiles

