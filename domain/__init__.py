from typing import List

from monads.either import Result, Ok
from monads.option import Option, Nothing, Some

# Original domain


class ValidationError:
    def __init__(self, message):
        self.message = message


class UnvalidatedOrder:
    pass


class ValidatedOrder:
    pass


class PricingError:
    def __init__(self, message):
        self.message = message


class PricedOrder:
    pass


class OrderAcknowledgementSent:
    pass


class PlaceOrderEvent:
    pass


def validate_order(
    unvalidated_order: UnvalidatedOrder
) -> Result[ValidatedOrder, ValidationError]:
    return Ok(ValidatedOrder())


def price_order(validated_order: ValidatedOrder) -> Result[PricedOrder, PricingError]:
    return Ok(PricedOrder())


def acknowledge_order(priced_order: PricedOrder) -> Option[OrderAcknowledgementSent]:
    return Some(OrderAcknowledgementSent())


def create_events(priced_order: PricedOrder) -> List[PlaceOrderEvent]:
    return []


# Converges error types for function composition


class PlaceOrderError:
    pass


class Validation(PlaceOrderError):
    def __init__(self, validation_error):
        self.validation_error = validation_error


class Pricing(PlaceOrderError):
    def __init__(self, pricing_error):
        self.pricing_error = pricing_error


#  Adapted to return a PlaceOrderError
def price_order_adapted(input: ValidatedOrder) -> Result[PricedOrder, PlaceOrderError]:
    return price_order(input).map_error(Pricing)


#  Adapted to return a PlaceOrderError
def validate_order_adapted(
    input: UnvalidatedOrder
) -> Result[ValidatedOrder, PlaceOrderError]:
    return validate_order(input).map_error(Validation)


#  Compose functions in our pipeline


def place_order(
    unvalidated_order: UnvalidatedOrder
) -> Result[List[PlaceOrderEvent], PlaceOrderError]:
    return (
        validate_order_adapted(unvalidated_order)
        .bind(price_order_adapted)
        .map(acknowledge_order)
        .map(create_events)
    )
