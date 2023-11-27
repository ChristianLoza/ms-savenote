from web3 import Web3
from kafka import KafkaConsumer
import json

# Configurar el consumidor Kafka
consumer = KafkaConsumer('TOPIC_MAIL', bootstrap_servers=['localhost:9093'])

# URL del nodo Ethereum de Sepolia
URL_DEL_NODO_ETH = "https://eth-sepolia.g.alchemy.com/v2/VqTlF6ORKjhjct9N0ldF_GDB92afAq9l"

# Dirección del contrato inteligente desplegado
DIRECCION_DEL_CONTRATO = Web3.to_checksum_address('0x8B021EF0404dAE0F566aF78B542BBD77356aF57c')

# Crear una conexión con el nodo Ethereum
web3 = Web3(Web3.HTTPProvider(URL_DEL_NODO_ETH))

abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "idExamen", "type": "string"},
            {"internalType": "string", "name": "nuevaNota", "type": "string"},
        ],
        "name": "actualizarNota",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "idExamen", "type": "string"},
            {"internalType": "string", "name": "nota", "type": "string"},
        ],
        "name": "guardarNota",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "", "type": "string"}],
        "name": "notasDeExamenes",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "idExamen", "type": "string"}],
        "name": "obtenerNota",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]
contrato = web3.eth.contract(address=DIRECCION_DEL_CONTRATO, abi=abi)

# Función para publicar una nueva nota de examen
def publicar_nota(id_examen, nota):
    # Transacción para la función 'guardarNota' del contrato
    transaccion = contrato.functions.guardarNota(id_examen, nota).build_transaction(
        {
            "gas": 100000,
            "gasPrice": web3.to_wei("20", "gwei"),
            "nonce": web3.eth.get_transaction_count("0xFDF6AE392C4A06C7A29F8340c08a724b484E0477"),
        }
    )

    # Firmar la transacción con tu clave privada
    #Account 1
    #transaccion_firmada = web3.eth.account.sign_transaction(
    #    transaccion, "24107b73d93391c874fffeab720079daee78078725a639cefd2ac5b61d593006"
    #)
    #Account2
    transaccion_firmada = web3.eth.account.sign_transaction(
        transaccion, "24107b73d93391c874fffeab720079daee78078725a639cefd2ac5b61d593006"
    )

    # Enviar la transacción
    transaccion_hash = web3.eth.send_raw_transaction(transaccion_firmada.rawTransaction)
    return transaccion_hash

for message in consumer:
    event = json.loads(message.value.decode('utf-8'))  # Suponiendo que los eventos están codificados en utf-8
    print(event)
    print('voy a intentar guardar una nota')
    contact = event['contact']
    score = str(event['score'])
    transaccion_hash = publicar_nota(contact, score)
    print(f"Transacción para publicar nota: {transaccion_hash.hex()}")
