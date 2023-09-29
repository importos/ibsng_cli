arguments=[
    
]
def call(ibsapi,arguments):
    resA,_ =  ibsapi.ras.getActiveRasIPs()
    resB,_ =  ibsapi.ras.getInActiveRases()
    return (resA,resB)

