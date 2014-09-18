#include <Adafruit_NeoPixel.h>

#define PIN 6

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(14, PIN, NEO_GRB + NEO_KHZ800);
boolean handshaken = false;

#define MAXWIDTH 50
char row[MAXWIDTH];
char ack;

void set_led(uint8_t index, uint8_t r, uint8_t g, uint8_t b) {
  uint32_t color = strip.Color(r, g, b);
  strip.setPixelColor(index, color);
  strip.show();
}


void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  Serial.begin(9600);
  while (!handshaken) {
    delay(100);
    heartbeat();
    while (Serial.available()) {
      ack = Serial.read();
      if (ack == '1') {
        handshaken = true;
        Serial.println('Handshake complete. Ready to consume commands.');
      }
    }
  }
}

void heartbeat() {
  Serial.println('PING');
}


void loop() {
}


void parse_command() {
  String strrow = String(row);
  if (strrow.startsWith("LED", 0)) {
    handle_led_command(strrow.substring(3));
  }
}


int pos = 0;
void serialEvent() {
    Serial.readBytesUntil('\n', row, MAXWIDTH);
    parse_command();
    for (int i = 0; i < MAXWIDTH; i++)
    {
      row[i] = 0;
    }
}


void handle_led_command(String param) {
  uint8_t index = param.substring(0,2).toInt();

  uint8_t r = param.substring(2,5).toInt();
  uint8_t g = param.substring(5,8).toInt();
  uint8_t b = param.substring(8,11).toInt();
  set_led(index, r, g, b);
}



