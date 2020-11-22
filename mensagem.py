from typing import Any
from excecoes import TipoMensagemInvalida
from enum import Enum, unique


@unique
class TipoPermitidosDeMensagem(Enum):
    movimentacao = "movimentacao"
    desistencia = "desistencia"
    chat = "chat"
    vencedor = "vencedor"
    conexao_estabelecida = "conexao_estabelecida"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, TipoPermitidosDeMensagem))


class Mensagem:
    def __init__(self, tipo: str, conteudo: Any, remetente: str):
        self._eh_um_tipo_valido(tipo_mensagem=tipo)
        self._conteudo: Any = conteudo
        self._tipo: str = tipo
        self._remetente: str = remetente

    def __str__(self):
        return f"tipo: {self._tipo}, conteudo: {self._conteudo}, remetente: {self.remetente}"

    @property
    def remetente(self) -> str:
        return self._remetente

    @property
    def conteudo(self) -> str:
        return self._conteudo

    @conteudo.setter
    def conteudo(self, novo_valor) -> None:
        self._conteudo = novo_valor

    @property
    def tipo(self) -> str:
        return self._tipo

    @conteudo.setter
    def conteudo(self, novo_valor) -> None:
        self._conteudo = novo_valor

    def _eh_um_tipo_valido(self, tipo_mensagem: str):
        if tipo_mensagem in TipoPermitidosDeMensagem.list():
            return True

        raise TipoMensagemInvalida(
            f"Esse tipo de mensagem é inválida. Tipos permitidos: {TipoPermitidosDeMensagem.list()}"
        )

    def setar_valores_da_classe(self, json_da_mensagem: dict) -> None:
        self._eh_um_tipo_valido(json_da_mensagem.get("tipo"))
        self._conteudo = json_da_mensagem.get("conteudo")
        self._tipo = json_da_mensagem.get("tipo")
        self._remetente = json_da_mensagem.get("remetente")

    def converter_msg_em_dict_para_enviar(self) -> dict:
        msg = {
            "tipo": self._tipo,
            "conteudo": self._conteudo,
            "remetente": self.remetente,
        }
        return msg
