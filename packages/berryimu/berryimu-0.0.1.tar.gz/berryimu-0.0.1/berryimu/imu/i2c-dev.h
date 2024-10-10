/*
    i2c-dev.h - i2c-bus driver, char device interface

    Copyright (C) 1995-97 Simon G. Vogl
    Copyright (C) 1998-99 Frodo Looijaard <frodol@dds.nl>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301 USA.
*/

#pragma once

#ifdef __linux__
#include "linux/types.h"
#else
#include <stdint.h>
typedef int32_t __s32;
typedef uint8_t __u8;
typedef uint16_t __u16;
typedef uint32_t __u32;
#endif

#include <stddef.h>
#include <sys/ioctl.h>

struct i2c_msg {
  __u16 addr;
  unsigned short flags;
#define I2C_M_TEN 0x10
#define I2C_M_RD 0x01
#define I2C_M_NOSTART 0x4000
#define I2C_M_REV_DIR_ADDR 0x2000
#define I2C_M_IGNORE_NAK 0x1000
#define I2C_M_NO_RD_ACK 0x0800
  short len;
  char *buf;
};

#define I2C_FUNC_I2C 0x00000001
#define I2C_FUNC_10BIT_ADDR 0x00000002
#define I2C_FUNC_PROTOCOL_MANGLING 0x00000004
#define I2C_FUNC_SMBUS_PEC 0x00000008
#define I2C_FUNC_SMBUS_BLOCK_PROC_CALL 0x00008000
#define I2C_FUNC_SMBUS_QUICK 0x00010000
#define I2C_FUNC_SMBUS_READ_BYTE 0x00020000
#define I2C_FUNC_SMBUS_WRITE_BYTE 0x00040000
#define I2C_FUNC_SMBUS_READ_BYTE_DATA 0x00080000
#define I2C_FUNC_SMBUS_WRITE_BYTE_DATA 0x00100000
#define I2C_FUNC_SMBUS_READ_WORD_DATA 0x00200000
#define I2C_FUNC_SMBUS_WRITE_WORD_DATA 0x00400000
#define I2C_FUNC_SMBUS_PROC_CALL 0x00800000
#define I2C_FUNC_SMBUS_READ_BLOCK_DATA 0x01000000
#define I2C_FUNC_SMBUS_WRITE_BLOCK_DATA 0x02000000
#define I2C_FUNC_SMBUS_READ_I2C_BLOCK 0x04000000
#define I2C_FUNC_SMBUS_WRITE_I2C_BLOCK 0x08000000

#define I2C_FUNC_SMBUS_BYTE                                                    \
  (I2C_FUNC_SMBUS_READ_BYTE | I2C_FUNC_SMBUS_WRITE_BYTE)
#define I2C_FUNC_SMBUS_BYTE_DATA                                               \
  (I2C_FUNC_SMBUS_READ_BYTE_DATA | I2C_FUNC_SMBUS_WRITE_BYTE_DATA)
#define I2C_FUNC_SMBUS_WORD_DATA                                               \
  (I2C_FUNC_SMBUS_READ_WORD_DATA | I2C_FUNC_SMBUS_WRITE_WORD_DATA)
#define I2C_FUNC_SMBUS_BLOCK_DATA                                              \
  (I2C_FUNC_SMBUS_READ_BLOCK_DATA | I2C_FUNC_SMBUS_WRITE_BLOCK_DATA)
#define I2C_FUNC_SMBUS_I2C_BLOCK                                               \
  (I2C_FUNC_SMBUS_READ_I2C_BLOCK | I2C_FUNC_SMBUS_WRITE_I2C_BLOCK)

#define I2C_FUNC_SMBUS_HWPEC_CALC I2C_FUNC_SMBUS_PEC

#define I2C_SMBUS_BLOCK_MAX 32
#define I2C_SMBUS_I2C_BLOCK_MAX 32

union i2c_smbus_data {
  __u8 byte;
  __u16 word;
  __u8 block[I2C_SMBUS_BLOCK_MAX + 2];
};

#define I2C_SMBUS_READ 1
#define I2C_SMBUS_WRITE 0

#define I2C_SMBUS_QUICK 0
#define I2C_SMBUS_BYTE 1
#define I2C_SMBUS_BYTE_DATA 2
#define I2C_SMBUS_WORD_DATA 3
#define I2C_SMBUS_PROC_CALL 4
#define I2C_SMBUS_BLOCK_DATA 5
#define I2C_SMBUS_I2C_BLOCK_BROKEN 6
#define I2C_SMBUS_BLOCK_PROC_CALL 7
#define I2C_SMBUS_I2C_BLOCK_DATA 8

#define I2C_RETRIES 0x0701
#define I2C_TIMEOUT 0x0702

#define I2C_SLAVE 0x0703
#define I2C_SLAVE_FORCE 0x0706
#define I2C_TENBIT 0x0704

#define I2C_FUNCS 0x0705

#define I2C_RDWR 0x0707

#define I2C_PEC 0x0708
#define I2C_SMBUS 0x0720

struct i2c_smbus_ioctl_data {
  __u8 read_write;
  __u8 command;
  __u32 size;
  union i2c_smbus_data *data;
};

struct i2c_rdwr_ioctl_data {
  struct i2c_msg *msgs;
  __u32 nmsgs;
};

#define I2C_RDRW_IOCTL_MAX_MSGS 42

static inline __s32 i2c_smbus_access(int file, char read_write, __u8 command,
                                     int size, union i2c_smbus_data *data) {
  struct i2c_smbus_ioctl_data args;

  args.read_write = read_write;
  args.command = command;
  args.size = size;
  args.data = data;
  return ioctl(file, I2C_SMBUS, &args);
}

static inline __s32 i2c_smbus_write_quick(int file, __u8 value) {
  return i2c_smbus_access(file, value, 0, I2C_SMBUS_QUICK, NULL);
}

static inline __s32 i2c_smbus_read_byte(int file) {
  union i2c_smbus_data data;
  if (i2c_smbus_access(file, I2C_SMBUS_READ, 0, I2C_SMBUS_BYTE, &data))
    return -1;
  else
    return 0x0FF & data.byte;
}

static inline __s32 i2c_smbus_write_byte(int file, __u8 value) {
  return i2c_smbus_access(file, I2C_SMBUS_WRITE, value, I2C_SMBUS_BYTE, NULL);
}

static inline __s32 i2c_smbus_read_byte_data(int file, __u8 command) {
  union i2c_smbus_data data;
  if (i2c_smbus_access(file, I2C_SMBUS_READ, command, I2C_SMBUS_BYTE_DATA,
                       &data))
    return -1;
  else
    return 0x0FF & data.byte;
}

static inline __s32 i2c_smbus_write_byte_data(int file, __u8 command,
                                              __u8 value) {
  union i2c_smbus_data data;
  data.byte = value;
  return i2c_smbus_access(file, I2C_SMBUS_WRITE, command, I2C_SMBUS_BYTE_DATA,
                          &data);
}

static inline __s32 i2c_smbus_read_word_data(int file, __u8 command) {
  union i2c_smbus_data data;
  if (i2c_smbus_access(file, I2C_SMBUS_READ, command, I2C_SMBUS_WORD_DATA,
                       &data))
    return -1;
  else
    return 0x0FFFF & data.word;
}

static inline __s32 i2c_smbus_write_word_data(int file, __u8 command,
                                              __u16 value) {
  union i2c_smbus_data data;
  data.word = value;
  return i2c_smbus_access(file, I2C_SMBUS_WRITE, command, I2C_SMBUS_WORD_DATA,
                          &data);
}

static inline __s32 i2c_smbus_process_call(int file, __u8 command,
                                           __u16 value) {
  union i2c_smbus_data data;
  data.word = value;
  if (i2c_smbus_access(file, I2C_SMBUS_WRITE, command, I2C_SMBUS_PROC_CALL,
                       &data))
    return -1;
  else
    return 0x0FFFF & data.word;
}

/* Returns the number of read bytes */
static inline __s32 i2c_smbus_read_block_data(int file, __u8 command,
                                              __u8 *values) {
  union i2c_smbus_data data;
  int i;
  if (i2c_smbus_access(file, I2C_SMBUS_READ, command, I2C_SMBUS_BLOCK_DATA,
                       &data))
    return -1;
  else {
    for (i = 1; i <= data.block[0]; i++)
      values[i - 1] = data.block[i];
    return data.block[0];
  }
}

static inline __s32 i2c_smbus_write_block_data(int file, __u8 command,
                                               __u8 length,
                                               const __u8 *values) {
  union i2c_smbus_data data;
  int i;
  if (length > 32)
    length = 32;
  for (i = 1; i <= length; i++)
    data.block[i] = values[i - 1];
  data.block[0] = length;
  return i2c_smbus_access(file, I2C_SMBUS_WRITE, command, I2C_SMBUS_BLOCK_DATA,
                          &data);
}

static inline __s32 i2c_smbus_read_i2c_block_data(int file, __u8 command,
                                                  __u8 length, __u8 *values) {
  union i2c_smbus_data data;
  int i;

  if (length > 32)
    length = 32;
  data.block[0] = length;
  if (i2c_smbus_access(file, I2C_SMBUS_READ, command,
                       length == 32 ? I2C_SMBUS_I2C_BLOCK_BROKEN
                                    : I2C_SMBUS_I2C_BLOCK_DATA,
                       &data))
    return -1;
  else {
    for (i = 1; i <= data.block[0]; i++)
      values[i - 1] = data.block[i];
    return data.block[0];
  }
}

static inline __s32 i2c_smbus_write_i2c_block_data(int file, __u8 command,
                                                   __u8 length,
                                                   const __u8 *values) {
  union i2c_smbus_data data;
  int i;
  if (length > 32)
    length = 32;
  for (i = 1; i <= length; i++)
    data.block[i] = values[i - 1];
  data.block[0] = length;
  return i2c_smbus_access(file, I2C_SMBUS_WRITE, command,
                          I2C_SMBUS_I2C_BLOCK_BROKEN, &data);
}

static inline __s32 i2c_smbus_block_process_call(int file, __u8 command,
                                                 __u8 length, __u8 *values) {
  union i2c_smbus_data data;
  int i;
  if (length > 32)
    length = 32;
  for (i = 1; i <= length; i++)
    data.block[i] = values[i - 1];
  data.block[0] = length;
  if (i2c_smbus_access(file, I2C_SMBUS_WRITE, command,
                       I2C_SMBUS_BLOCK_PROC_CALL, &data))
    return -1;
  else {
    for (i = 1; i <= data.block[0]; i++)
      values[i - 1] = data.block[i];
    return data.block[0];
  }
}
