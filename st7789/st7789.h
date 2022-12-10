
#ifndef __ST7789_H__
#define __ST7789_H__

#include "esp_lcd_panel_io.h"

//
// Default Values for T-Display-S3 170x320 ST7789
//

#define TFT_WIDTH 170
#define TFT_HEIGHT 320
#define TFT_MAX_TRANSFER (TFT_WIDTH * TFT_HEIGHT * sizeof(uint16_t))

#define TFT_POWER GPIO_NUM_15
#define TFT_RST GPIO_NUM_5
#define TFT_CS GPIO_NUM_6
#define TFT_DC GPIO_NUM_7
#define TFT_BL GPIO_NUM_38
#define TFT_WR GPIO_NUM_8
#define TFT_RD GPIO_NUM_9
#define TFT_D0 GPIO_NUM_39
#define TFT_D1 GPIO_NUM_40
#define TFT_D2 GPIO_NUM_41
#define TFT_D3 GPIO_NUM_42
#define TFT_D4 GPIO_NUM_45
#define TFT_D5 GPIO_NUM_46
#define TFT_D6 GPIO_NUM_47
#define TFT_D7 GPIO_NUM_48

// ST7789 Commands
#define ST7789_VSCRDEF 0x33
#define ST7789_VSCSAD  0x37

// Color definitions
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

// driver options
#define OPTIONS_WRAP_V 0x01
#define OPTIONS_WRAP_H 0x02
#define OPTIONS_WRAP   0x03

typedef struct _Point {
    mp_float_t x;
    mp_float_t y;
} Point;

typedef struct _Polygon {
    int length;
    Point *points;
} Polygon;

typedef struct _st7789_rotation_t {
    uint16_t width;     // width of the display in this rotation
    uint16_t height;    // height of the display in this rotation
    uint16_t x_gap;     // gap on x axis, in pixels
    uint16_t y_gap;     // gap on y axis, in pixels
    bool swap_xy;       // set MADCTL_MV bit 0x20
    bool mirror_x;      // set MADCTL MX bit 0x40
    bool mirror_y;      // set MADCTL MY bit 0x80
} st7789_rotation_t;


typedef struct _st7789_ST7789_obj_t {
    mp_obj_base_t base;

    esp_lcd_i80_bus_handle_t i80_bus;
    esp_lcd_panel_io_handle_t io_handle;
    esp_lcd_panel_handle_t panel_handle;

    mp_file_t *fp;                                  // file object
    size_t frame_buffer_size;                       // frame buffer size in bytes
    uint16_t *frame_buffer;                         // frame buffer
    uint16_t *work_buffer;                          // work frame buffer
    // m_malloc'd pointers
    void *work;                                     // work buffer for jpg & png decoding
    uint8_t *scanline_ringbuf;                      // png scanline_ringbuf
    uint8_t *palette;                               // png palette
    uint8_t *trans_palette;                         // png trans_palette
    uint8_t *gamma_table;                           // png gamma_table

    uint16_t display_width;                         // physical width
    uint16_t display_height;                        // physical width

    uint16_t width;                                 // logical width (after rotation)
    uint16_t height;                                // logical height (after rotation)

    uint8_t colstart;
    uint8_t rowstart;
    uint8_t rotation;
    st7789_rotation_t *rotations;                   // list of rotation tuples [(madctl, colstart, rowstart)]
    uint8_t rotations_len;                          // number of rotations

    uint8_t options;                                // options bit array: wrap (optional)

	gpio_num_t power;
	gpio_num_t rst;
	gpio_num_t cs;
	gpio_num_t dc;
	gpio_num_t bl;
	gpio_num_t wr;
	gpio_num_t rd;
	gpio_num_t d0;
	gpio_num_t d1;
	gpio_num_t d2;
	gpio_num_t d3;
	gpio_num_t d4;
	gpio_num_t d5;
	gpio_num_t d6;
	gpio_num_t d7;

} st7789_ST7789_obj_t;

mp_obj_t st7789_ST7789_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

extern void draw_pixel(st7789_ST7789_obj_t *self, int16_t x, int16_t y, uint16_t color, uint8_t alpha);
extern void fast_hline(st7789_ST7789_obj_t *self, int16_t x, int16_t y, int16_t w, uint16_t color, uint8_t alpha);

#endif // __ST7789_H__