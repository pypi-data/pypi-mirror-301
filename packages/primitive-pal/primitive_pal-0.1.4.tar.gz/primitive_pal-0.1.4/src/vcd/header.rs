use std::fs::File;
use std::io::{self, BufReader, Read, Write};
use std::path::Path;

use crate::vcd::parser::Parser;

pub fn process_header(path: &Path) -> io::Result<Option<u64>> {
    // Extract filename
    let filename = match path.file_name() {
        Some(name) => format!("{}.json", name.to_string_lossy().into_owned()),
        None => "header.json".to_string(),
    };
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    let mut accumulated_buffer: Vec<u8> = Vec::new();
    let mut buffer = [0; 1024 * 1024]; // 1MB Buffer
    let mut leftover = String::new();
    let mut ptr: u64 = 0;

    'read_loop: while let Ok(bytes_read) = reader.read(&mut buffer) {
        if bytes_read == 0 {
            // EOF reached without finding data section
            return Ok(None);
        }

        // Add to accumulated buffer
        let bytes = &buffer[..bytes_read];
        accumulated_buffer.extend_from_slice(bytes);

        let chunk = String::from_utf8_lossy(bytes);
        let chunk = format!("{}{}", leftover, chunk);
        let lines = chunk.lines();

        for line in lines.clone() {
            let line_length = line.len() as u64 + 1; // Add one for new line character

            if line == "$dumpvars" {
                break 'read_loop;
            }

            ptr += line_length;
        }

        // If we didn't end on a newline
        if !chunk.ends_with("\n") {
            leftover = lines.last().unwrap_or("").to_string();
        } else {
            leftover.clear();
        }
    }

    // Parse
    let mut parser = Parser::new(accumulated_buffer.as_slice(), false);
    let header = parser.parse_header()?;

    // Write header to file
    let json_header = serde_json::to_string(&header)?;
    let mut file = File::create(filename)?;
    file.write_all(json_header.as_bytes())?;

    Ok(Some(ptr))
}
