import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================
def test_bug_1_subtotal_multiplica_preco_por_quantidade(pedido_pequeno):
    # 1 café (6.0) + 2 pães de queijo (4.5 cada) = 15.0
    assert pedido_pequeno.subtotal() == 15.0

def test_bug_2_frete_gratis_com_subtotal_exatamente_50():
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True

def test_bug_3_item_mais_barato_retorna_menor_preco(pedido_pequeno):
    assert pedido_pequeno.item_mais_barato() == Item("Pão de queijo", 4.5, 2)


def test_bug_4_total_com_desconto_subtrai_percentual():
    pedido = Pedido("Carla", [Item("Cento de salgado", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0
# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função

def test_contar_frete_gratis_todos_com_frete_gratis(pedido_grande):
    outro_grande = Pedido("Carlos", [Item("Combo Família", 60.0, 1)])
    assert contar_frete_gratis([pedido_grande, outro_grande]) == 2


def test_contar_frete_gratis_nenhum_com_frete_gratis(pedido_pequeno):
    outro_pequeno = Pedido("Carla", [Item("Suco", 8.0, 1)])
    assert contar_frete_gratis([pedido_pequeno, outro_pequeno]) == 0


def test_contar_frete_gratis_lista_mista(pedido_pequeno, pedido_grande):
    assert contar_frete_gratis([pedido_pequeno, pedido_grande]) == 1


def test_contar_frete_gratis_lista_vazia():
    assert contar_frete_gratis([]) == 0

# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método

def test_situacao_mais_de_25_porcento_indisponivel_com_frete_gratis(pedido_grande):
    # pedido_grande tem 5 unidades; 2 indisponíveis = 40% (> 25%)
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_situacao_tudo_disponivel_com_frete_gratis(pedido_grande):
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_situacao_tudo_disponivel_sem_frete_gratis(pedido_pequeno):
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_situacao_exatamente_25_porcento_indisponivel_segue_regra_do_frete():
    # 4 unidades de R$ 20,00 (subtotal R$ 80,00) e 1 indisponível = exatamente 25%
    pedido = Pedido("Carla", [Item("Hambúrguer", 20.0, 4)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"


def test_situacao_pouco_acima_de_25_porcento_indisponivel():
    # 100 unidades e 26 indisponíveis = 26% (pouco acima de 25%)
    pedido = Pedido("Carla", [Item("Salgadinho", 1.0, 100)])
    assert pedido.situacao(26) == "Cancelado por falta de estoque"

# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
