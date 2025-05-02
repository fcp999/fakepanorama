# fakepanorama
oci server fake panorama to enable block option to appear for iocs - it doesn't do anything else.
listens on 8081 unless you change it 
you may have to enable the port in the firewall 

I put it on the oci server in rtm/bin and add to the top of start in that dir
python3 fp.py &

or run it alone if you are using tmux

on OCI use http://127.0.0.1:8081  as Panorama url
if all is green then select new Panorama and Activate.



