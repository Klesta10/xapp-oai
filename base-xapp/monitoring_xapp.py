import xapp_control_ricbypass
from e2sm_proto import *
from time import sleep

def main():    

    print("Encoding ric monitoring request")
    
    # external message
    master_mess = RAN_message()
    master_mess.msg_type = RAN_message_type.INDICATION_REQUEST

    # internal message
    inner_mess = RAN_indication_request()
    inner_mess.target_params.extend([RAN_parameter.GNB_ID, RAN_parameter.UE_LIST])


    # assign and serialize
    master_mess.ran_indication_request.CopyFrom(inner_mess)
    buf = master_mess.SerializeToString()
    buf = master_mess.SerializeToString()
    xapp_control_ricbypass.send_to_socket(buf)
    
    while True:
        r_buf = xapp_control_ricbypass.receive_from_socket()
        ran_ind_resp = RAN_indication_response()
        ran_ind_resp.ParseFromString(r_buf)

        # Check if the received BER is higher than the threshold
        threshold = 0.5  # Define the BER threshold
        if ran_ind_resp.ber > threshold:
            print("Received BER is higher than the threshold. Sending control request.")



if __name__ == '__main__':
    main()

