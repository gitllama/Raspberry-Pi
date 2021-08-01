use rppal::i2c::I2c;
use byteorder::{BigEndian, ByteOrder};
use std::str;
use std::{thread, time::Duration};

#[macro_use]
extern crate clap;
use clap::App;

const ADDR: u16 = 0x5A;

const READ_START: u8 = 0x15;
const READ_STOP: u8 = 0x25;
const READ_DATA_LENGTH: u8 = 0x35;
const READ_DATA: u8 = 0x45;
const WRITE_DATA_LENGTH: u8 = 0x19;
const WRITE_DATA: u8 = 0x29;
const SEND_DATA: u8 = 0x39;
const SLEEP_TIME:u64 = 5;

fn read_command() -> Result<u8, rppal::i2c::Error>{
    
    
    let mut i2c = I2c::with_bus(1)?;
    //i2c.set_timeout(100)?;
    i2c.set_slave_address(ADDR)?;
    
    println!("read start");
    i2c.smbus_send_byte(READ_START)?;
    thread::sleep(Duration::from_secs(SLEEP_TIME));
    i2c.smbus_send_byte(READ_STOP)?;
    println!("read end");
     
    let mut buf_length:[u8;3] = Default::default();
    i2c.block_read(READ_DATA_LENGTH, &mut buf_length)?;
    let data_length:i32 = BigEndian::read_u16(&buf_length[1..3]) as i32;
    //let data_length:i32 = (buf_length[1] as i32) << 8 | (buf_length[2] as i32);
    
    println!("{:?}, {}",buf_length, data_length);

    //if(data_length >= 65535){ Err(None); }

    let mut result = String::from("");
    let mut buf:[u8;1] = Default::default();

    i2c.block_read(READ_DATA, &mut buf)?;
    for _i in 0..data_length{
        let mut data:[u8;4] = Default::default();
        i2c.block_read(READ_DATA, &mut data)?;
        let data_str = format!("{:<08X}", BigEndian::read_u32(&data)); 
        // let data_str = format!("{:<02X}{:<02X}{:<02X}{:<02X}",data[0], data[1], data[2], data[3]);
        result.push_str(data_str.as_str());
    }

    println!("{}",result);
    Ok(0)
}

fn write_command(val:&str) -> Result<u8, rppal::i2c::Error>{

    let str_len = val.len();
    let byte_len = str_len/2;
    let u32_len = byte_len/4;
    
    let mut i2c = I2c::with_bus(1)?;
    //i2c.set_timeout(100)?;
    i2c.set_slave_address(ADDR)?;
    
    println!("write start");
    let mut data_length:[u8;2] = Default::default();
    BigEndian::write_u16(&mut data_length, u32_len as u16);
    i2c.block_write(WRITE_DATA_LENGTH, &data_length)?;
    println!("length : {:?} {:?}", data_length, u32_len);

    for _i in (0..str_len).step_by(2*4){
        let mut data:[u8;4] = Default::default();
        let n = u32::from_str_radix(&val[_i.._i+8], 16).unwrap();
        BigEndian::write_u32(&mut data, n);
        //println!("{:?}",data);
        i2c.block_write(WRITE_DATA, &data)?;
    }

    println!("send!");
    i2c.smbus_send_byte(SEND_DATA)?;

    Ok(0)
}

fn main() {

    let yaml = load_yaml!("cli.yml");
    let matches = App::from_yaml(yaml).get_matches();
    
    if matches.is_present("read") {
        let result = read_command();
        match result{
            Ok(n) => println!("Done : {}", n),
            Err(e) => println!("Error : {}", e),
        };
    }

    if let Some(o) = matches.value_of("write") {
        let result = write_command(o);
        match result{
            Ok(n) => println!("Done : {}", n),
            Err(e) => println!("Error : {}", e),
        };
    }

}
