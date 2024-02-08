import test_cpu
import constants

def modem(device=constants.DEVICE_IP):
    pass

def cpu(device=constants.DEVICE_IP):
    cpu_result = test_cpu.main(device=device)

    if cpu_result["success"]:
        print("CPU: [OK]")
    else:
        print("CPU: [KO]")

if __name__ == "__main__":
    ## CPU ###
    cpu()

    ## TODO: GPU
    
    ## TODO: Modem (3G/4G) ###

        
    
    ## TODO: Wifi ###
        
    ## TODO: Screen ###
        
    ## TODO: GPS ###
        
    ## TODO: port USB ###