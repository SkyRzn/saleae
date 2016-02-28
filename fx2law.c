/*
 * fx2law
 *
 * Copyright (c) 2016 Alexandr Ivanov (alexandr.sky@gmail.com)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <linux/module.h>
#include <linux/usb.h>


#define USB_VENDOR_ID_SALEAE	0x0925
#define USB_PRODUCT_ID_SALEAE	0x3881


static const struct usb_device_id fx2law_id[] = {
	{USB_DEVICE(USB_VENDOR_ID_SALEAE, USB_PRODUCT_ID_SALEAE)},
	{}
};


int fx2law_probe(struct usb_interface *intf, const struct usb_device_id *id)
{
	printk(KERN_ALERT "PROBE\n");
	return 0;
}

void fx2law_disconnect(struct usb_interface *intf)
{
	printk(KERN_ALERT "DISCONNECT\n");
}

static struct usb_driver fx2law_driver = {
	.probe = fx2law_probe,
	.disconnect = fx2law_disconnect,
	.name = "fx2law",
	.id_table = fx2law_id,
};

module_usb_driver(fx2law_driver);


MODULE_AUTHOR("Alexandr Ivanov <alexandr.sky@gmail.com>");
MODULE_DESCRIPTION("FX2LAW driver");
MODULE_LICENSE("GPL");
