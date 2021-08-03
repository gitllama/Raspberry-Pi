use rppal::i2c::I2c;
use byteorder::{BigEndian, ByteOrder};
use std::str;
use std::{thread, time::Duration};
use serde_json::Value;
// use std::error::Error;
use std::fs::File;
use std::io::BufReader;
//  use std::path::Path;

#[macro_use]
extern crate clap;
use clap::App;


struct RaspiI2c {
    i2c : I2c
}

impl RaspiI2c {
    const ADDR: u16 = 0x5A;
    
    const READ_START: u8 = 0x15;
    const READ_STOP: u8 = 0x25;
    const READ_DATA_LENGTH: u8 = 0x35;
    const READ_DATA: u8 = 0x45;
    const WRITE_DATA_LENGTH: u8 = 0x19;
    const WRITE_DATA: u8 = 0x29;
    const SEND_DATA: u8 = 0x39;
    
    pub fn init() -> Result<RaspiI2c, rppal::i2c::Error> {
        let mut dst = RaspiI2c{ 
            i2c : I2c::with_bus(1)?
        };
        // i2c.set_timeout(100)?;
        dst.i2c.set_slave_address(Self::ADDR)?;
        Ok(dst)
    }
    
    pub fn str2vec(val:&str) -> Vec<u32> {
        let mut vec:Vec<u32> = Vec::new();
        
        let str_len = val.len();
        // let byte_len = str_len/2;
        // let u32_len = byte_len/4;
        
        for _i in (0..str_len).step_by(2*4){
            let n = u32::from_str_radix(&val[_i.._i+8], 16).unwrap();
            vec.push(n);
        }
        vec
    }
    
    pub fn vec2str(val:Vec<u32>) -> String {
        let mut result = String::from("");
        for _i in 0..val.len(){
            let data_str = format!("{:<08X}", val[_i]); 
            result.push_str(data_str.as_str());
        }
        result
        //let data_str = format!("{:<08X}", BigEndian::read_u32(&data)); 
    }
    
    pub fn receive(&self, sleep_time:u64)-> Result<i32, rppal::i2c::Error>{
        self.i2c.smbus_send_byte(Self::READ_START)?;
        thread::sleep(Duration::from_secs(sleep_time));
        self.i2c.smbus_send_byte(Self::READ_STOP)?;
        
        let mut buf_length:[u8;3] = Default::default();
        self.i2c.block_read(Self::READ_DATA_LENGTH, &mut buf_length)?;
        let data_length:i32 = BigEndian::read_u16(&buf_length[1..3]) as i32;
        // println!("{:?}, {}",buf_length, data_length);
        // if(data_length >= 65535){ Err(None); }
        Ok(data_length)
    }
    
    pub fn trans_receive(&self, data_length:i32)-> Result<Vec<u32>, rppal::i2c::Error>{
        let mut vec:Vec<u32> = Vec::new();
        let mut buf:[u8;1] = Default::default();
        self.i2c.block_read(Self::READ_DATA, &mut buf)?;
        for _i in 0..data_length{
            let mut data:[u8;4] = Default::default();
            self.i2c.block_read(Self::READ_DATA, &mut data)?;
            vec.push(BigEndian::read_u32(&data));
        }
        Ok(vec)
    }
    
    pub fn send(&self, vec:Vec<u32>)-> Result<u8, rppal::i2c::Error>{
        let u32_len = vec.len() as u16;
        let mut data_length:[u8;2] = Default::default();
        BigEndian::write_u16(&mut data_length, u32_len);
        println!("length : {:?} {:?}", u32_len, data_length);

        println!("write start");
        self.i2c.block_write(Self::WRITE_DATA_LENGTH, &data_length)?;
        for _i in 0..vec.len(){
            let mut data:[u8;4] = Default::default();
            BigEndian::write_u32(&mut data, vec[_i]);
            // println!("{:?}",data);
            self.i2c.block_write(Self::WRITE_DATA, &data)?;
        }

        println!("send!");
        self.i2c.smbus_send_byte(Self::SEND_DATA)?;
        
        Ok(0)
    }
}


fn read_command(sleep_time:u64) -> Result<u8, rppal::i2c::Error>{
    
    let i2c = RaspiI2c::init()?;
    println!("read start");
    let data_length = i2c.receive(sleep_time)?;
    println!("read end : {}", data_length);
    let result = i2c.trans_receive(data_length)?;
    // println!("{:?}",result);
    println!("[{}]",RaspiI2c::vec2str(result));
    Ok(0)

}

fn write_command(val:&str) -> Result<u8, rppal::i2c::Error>{
    
    let i2c = RaspiI2c::init()?;
    let vac = RaspiI2c::str2vec(&val);
    i2c.send(vac)?;
    
    Ok(0)

}


fn main() {

    let yaml = load_yaml!("cli.yml");
    let matches = App::from_yaml(yaml).get_matches();

    if matches.is_present("list") { 
        let paths = matches.value_of("config").unwrap();
        let file = File::open(paths).unwrap();
        let reader = BufReader::new(file);
        let json: Value = serde_json::from_reader(reader).unwrap();
        println!("{:?}", json);
        return;
    }    
    
    if matches.is_present("read") { 
        let str_time = matches.value_of("wait").unwrap();
        let sleep_time: u64 = str_time.parse().unwrap();
        let result = read_command(sleep_time);
        match result{
            Ok(n) => println!("Done : {}", n),
            Err(e) => println!("Error : {}", e),
        };
    }

    if let Some(o) = matches.value_of("send") {
        let result = write_command(o);
        match result{
            Ok(n) => println!("Done : {}", n),
            Err(e) => println!("Error : {}", e),
        };
    }

    if let Some(os) = matches.values_of("key") {
        // for o in os { println!("key: {}", o); }
        // matches.values_of("key").unwarp().collect();
        
        let paths = matches.value_of("config").unwrap();
        let file = File::open(paths).unwrap();
        let reader = BufReader::new(file);
        let json: Value = serde_json::from_reader(reader).unwrap();
        let a: Vec<_> = os.collect();
        println!("key: {} {}",a[0], a[1]);
        let result = write_command(json[a[0]][a[1]].as_str().unwrap());
        match result{
            Ok(n) => println!("Done : {}", n),
            Err(e) => println!("Error : {}", e),
        };
    }

}
