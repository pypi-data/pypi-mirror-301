# conversor.py

class ConversorBinario:
    @staticmethod
    def binario_para_decimal(binario: str) -> int:
        """Converte número binário para decimal"""
        return int(binario, 2)

    @staticmethod
    def binario_para_octal(binario: str) -> str:
        """Converte número binário para octal"""
        decimal = int(binario, 2)
        return oct(decimal)

    @staticmethod
    def binario_para_hexadecimal(binario: str) -> str:
        """Converte número binário para hexadecimal"""
        decimal = int(binario, 2)
        return hex(decimal)
