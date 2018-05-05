# Sunfounder Smart Video Car Software Improved
I don't plan to change much more in client/client_my.py (originally client_App.py), neither functionally nor regarding code quality.  
Please check the comments for improvements.

On the server side (code running on the Raspberry Pi; server directory), tcp_server_my.py is partially revised, namely in the parts that have to match the client part.

tcp_server_my.py depends on motor_my.py and steer.py, where the latter originally is named car_dir.py. I changed this to steer.py instead of to car_dir_my.py because I think this is much better naming.
