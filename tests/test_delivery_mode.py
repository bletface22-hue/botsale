from app.models.entities import DeliveryMode


def test_delivery_modes_exist() -> None:
    assert DeliveryMode.icc_id_chat.value == "icc_id_chat"
    assert DeliveryMode.bot_chat.value == "bot_chat"
    assert DeliveryMode.auto_delivery.value == "auto_delivery"
