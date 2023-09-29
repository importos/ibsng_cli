arguments=[
    ("ip","ip")   
]
def call(ibsapi,arguments):
    resA,_ =  ibsapi.ras.deActiveRas(ras_ip=arguments["ip"])
    return resA

