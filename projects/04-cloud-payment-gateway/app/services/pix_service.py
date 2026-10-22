import io
import base64
import qrcode
from typing import Tuple

class PixPayloadEngine:
    """
    Motor de Geração de Códigos Pix no Padrão EMV (BR Code - Banco Central do Brasil).
    Calcula CRC16 polinomial (CCITT-FALSE) e empacota TLV (Tag-Length-Value).
    """

    ID_PAYLOAD_FORMAT_INDICATOR = "00"
    ID_MERCHANT_ACCOUNT_INFORMATION = "26"
    ID_MERCHANT_ACCOUNT_INFORMATION_GUI = "00"
    ID_MERCHANT_ACCOUNT_INFORMATION_KEY = "01"
    ID_MERCHANT_CATEGORY_CODE = "52"
    ID_TRANSACTION_CURRENCY = "53"
    ID_TRANSACTION_AMOUNT = "54"
    ID_COUNTRY_CODE = "58"
    ID_MERCHANT_NAME = "59"
    ID_MERCHANT_CITY = "60"
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE = "62"
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = "05"
    ID_CRC16 = "63"

    @staticmethod
    def _formatar_tlv(tag: str, valor: str) -> str:
        """Formata no padrão Tag-Length-Value: Tag (2 dígitos) + Tamanho (2 dígitos) + Valor."""
        tamanho = f"{len(valor):02d}"
        return f"{tag}{tamanho}{valor}"

    @classmethod
    def _calcular_crc16(cls, payload: str) -> str:
        """
        Calcula o checksum CRC16-CCITT (polinômio 0x1021, valor inicial 0xFFFF).
        Padrão obrigatório pelo Banco Central para validar integridade do Pix.
        """
        payload_para_calculo = f"{payload}{cls.ID_CRC16}04"
        crc = 0xFFFF
        for char in payload_para_calculo:
            crc ^= ord(char) << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
        return f"{crc:04X}"

    @classmethod
    def gerar_pix_copia_e_cola(
        cls,
        chave_pix: str,
        beneficiario: str,
        cidade: str,
        valor: float,
        txid: str
    ) -> str:
        """Gera a string completa do Pix Copia e Cola (EMV QR Code)."""
        # 1. Informações da Conta do Recebedor (Tag 26)
        gui = cls._formatar_tlv(cls.ID_MERCHANT_ACCOUNT_INFORMATION_GUI, "br.gov.bcb.pix")
        chave = cls._formatar_tlv(cls.ID_MERCHANT_ACCOUNT_INFORMATION_KEY, chave_pix)
        merchant_account = cls._formatar_tlv(cls.ID_MERCHANT_ACCOUNT_INFORMATION, f"{gui}{chave}")

        # 2. Dados adicionais (txid / Identificador da transação)
        txid_tlv = cls._formatar_tlv(cls.ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, txid[:25])
        additional_data = cls._formatar_tlv(cls.ID_ADDITIONAL_DATA_FIELD_TEMPLATE, txid_tlv)

        # 3. Montagem das tags base
        payload = (
            cls._formatar_tlv(cls.ID_PAYLOAD_FORMAT_INDICATOR, "01") +
            merchant_account +
            cls._formatar_tlv(cls.ID_MERCHANT_CATEGORY_CODE, "0000") +
            cls._formatar_tlv(cls.ID_TRANSACTION_CURRENCY, "986") +  # 986 = Real (BRL)
            cls._formatar_tlv(cls.ID_TRANSACTION_AMOUNT, f"{valor:.2f}") +
            cls._formatar_tlv(cls.ID_COUNTRY_CODE, "BR") +
            cls._formatar_tlv(cls.ID_MERCHANT_NAME, beneficiario[:25]) +
            cls._formatar_tlv(cls.ID_MERCHANT_CITY, cidade[:15]) +
            additional_data
        )

        # 4. Cálculo final do CRC16
        crc = cls._calcular_crc16(payload)
        return f"{payload}{cls.ID_CRC16}04{crc}"

    @staticmethod
    def gerar_qr_code_base64(payload_pix: str) -> str:
        """Renderiza a imagem do QR Code em memória e converte para Base64 PNG."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2
        )
        qr.add_data(payload_pix)
        qr.make(fit=True)

        img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"
