use std::convert::TryFrom;

// --- 1. Custom Error Enum for structured error reporting ---
#[derive(Debug)]
pub enum ConfigError {
    MissingField(String),
    InvalidType(String),
    RangeError(String, i32),
}

// --- 2. Target (Validated) Structure ---
#[derive(Debug)]
pub struct ServerConfig {
    pub name: String,
    pub port: u16,
    pub threads: u8,
}

// --- 3. Source (Raw/Unvalidated) Structure ---
#[derive(Debug)]
pub struct ConfigData {
    pub server_name: Option<String>,
    pub port_number: Option<i32>,
    pub worker_threads: Option<i32>,
}

// --- 4. Implementing the TryFrom Trait for Validation ---
impl TryFrom<ConfigData> for ServerConfig {
    type Error = ConfigError;

    fn try_from(raw_data: ConfigData) -> Result<Self, Self::Error> {
        // Use '?' operator (sugar for match/unwrap_or_else) to check and unwrap Option<T>
        let name = raw_data.server_name
            .ok_or(ConfigError::MissingField("server_name".to_string()))?;

        let raw_port = raw_data.port_number
            .ok_or(ConfigError::MissingField("port_number".to_string()))?;

        let raw_threads = raw_data.worker_threads
            .ok_or(ConfigError::MissingField("worker_threads".to_string()))?;

        // --- Port Validation (Range and Type Conversion) ---
        // 1. Check bounds on the i32 value first.
        if raw_port < 1024 || raw_port > 65535 {
            return Err(ConfigError::RangeError("port_number".to_string(), raw_port));
        }

        // 2. Now it's guaranteed to be in range and positive, safely convert to u16.
        let port = u16::try_from(raw_port)
            .map_err(|_| ConfigError::InvalidType(format!("port_number conversion error: {}", raw_port)))?;
        
        // (The original code's second check on u16 is now redundant and removed.)
        
        // --- Threads Validation (Range and Type Conversion) ---
        let threads = u8::try_from(raw_threads)
            .map_err(|_| ConfigError::InvalidType(format!("worker_threads value: {}", raw_threads)))?;

        if threads == 0 {
             return Err(ConfigError::RangeError("worker_threads".to_string(), raw_threads));
        }

        // Return the validated struct wrapped in Ok()
        Ok(ServerConfig {
            name,
            port,
            threads,
        })
    }
}

fn main() {
    println!("--- Test 1: Successful Conversion ---");
    let raw_good = ConfigData {
        server_name: Some("Prod-API".to_string()),
        port_number: Some(8080), 
        worker_threads: Some(16), 
    };

    match ServerConfig::try_from(raw_good) {
        Ok(config) => println!("✅ Config loaded successfully: {:?}", config),
        Err(e) => println!("❌ Config failed: {:?}", e),
    }

    println!("\n--- Test 2: Invalid Port Range ---");
    let raw_bad_port = ConfigData {
        server_name: Some("Test-API".to_string()),
        port_number: Some(80), // Below 1024
        worker_threads: Some(4),
    };

    match ServerConfig::try_from(raw_bad_port) {
        Ok(config) => println!("✅ Config loaded successfully: {:?}", config),
        Err(e) => println!("❌ Config failed: {:?}", e),
    }

    println!("\n--- Test 3: Missing Field ---");
    let raw_missing_name = ConfigData {
        server_name: None, // Missing
        port_number: Some(8081),
        worker_threads: Some(8),
    };

    match ServerConfig::try_from(raw_missing_name) {
        Ok(config) => println!("✅ Config loaded successfully: {:?}", config),
        Err(e) => println!("❌ Config failed: {:?}", e),
    }
}