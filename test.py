#!/usr/bin/python

import usb, struct


fw_path = '/usr/share/sigrok-firmware/fx2lafw-saleae-logic.fw'

MAX_SAMPLE_DELAY = 6 * 256
NUM_SIMUL_TRANSFERS	= 32


def fw_load(dev, filepath):
	print 'Firmware loading...'
	
	dev.ctrl_transfer(0x40, 0xa0, 0xe600, 0, '\01');

	offset = 0
	with open(filepath, 'r') as fw:
		while 1:
			chunk = fw.read(4096)
			if not chunk:
				break
			size = len(chunk)
			
			print '\twrite %d bytes from 0x%04x' % (size, offset)
						
			dev.ctrl_transfer(0x40, 0xa0, offset, 0, chunk);
			
			offset += size

	dev.ctrl_transfer(0x40, 0xa0, 0xe600, 0, '\00');
	
SR48 = 48000000
SR30 = 30000000
	
def calc_delay(samplerate):
	
	delay = 0
	sr = 0
	
	if (SR48 % samplerate) == 0:
		sr = SR48
		delay = sr / samplerate - 1
		if delay > MAX_SAMPLE_DELAY:
			delay = 0
	

	if delay == 0 and (SR30 % samplerate) == 0:
		sr = SR30
		delay = sr / samplerate - 1
	
	return delay, sr

#def calc_bytes_per_ms(samplerate):
	#return samplerate / 1000

#def calc_buffer_size(samplerate):
	#s = 10 * calc_bytes_per_ms(samplerate)
	#return (s + 511) & ~511;

#def calc_number_of_transfers(samplerate):
	#n = 500 * calc_bytes_per_ms(samplerate) / calc_buffer_size(samplerate)
	#if n > NUM_SIMUL_TRANSFERS:
		#n = NUM_SIMUL_TRANSFERS
	#return n

#def calc_timeout(samplerate):
	#total_size = calc_buffer_size(samplerate) * calc_number_of_transfers(samplerate)
	#timeout = total_size / calc_bytes_per_ms(samplerate)
	#return timeout + timeout / 4

def send_start(dev, delay, sr):
	print 'send start'
	flags = 1<<6 if sr == SR48 else 0
	data = struct.pack('BBB', flags, (delay >> 8) & 0xff, delay & 0xff)
	dev.ctrl_transfer(0x40, 0xb1, 0x0000, 0x0000, data);

def pack_receive(dev, sample_count):
	print 'pack receive'
	ret = dev.read(0x82, sample_count)
	for r in ret:
		print '%02x ' % r,

def run(dev, sample_count, sample_rate):
	delay, sr = calc_delay(sample_rate)
	print 'delay=%d, sr=%d' % (delay, sr)

	send_start(dev, delay, sr)
	
	for i in range(1):
		pack_receive(dev, 4096)
	

def main():
	dev = usb.core.find(idVendor=0x0925, idProduct=0x3881)
	if dev is None:
		raise ValueError('Device not found')
	
	#print dev
	#return

	#dev.set_configuration()
	#cfg = dev.get_active_configuration()

	if not dev.iManufacturer and not dev.iProduct:
		fw_load(dev, fw_path)
		
	run(dev, 100, 20000)
	
main()