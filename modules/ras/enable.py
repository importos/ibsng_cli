arguments=[
    ("ip","ip")   
]
def call(ibsapi,arguments):
    resA,_ =  ibsapi.ras.reActiveRas(ras_ip=arguments["ip"])
    return resA

