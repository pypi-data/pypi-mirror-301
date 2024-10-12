import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import pendulum
from pydantic import Field
from supamodel._abc import BaseModel
from supamodel.enums import PositionStatus


class Portfolio(BaseModel):
    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier of the portfolio"
    )
    user_id: Optional[UUID] = Field(
        description="ID of the user associated with the portfolio"
    )
    name: str = Field(description="Name of the portfolio")
    exchange_id: Optional[UUID] = Field(
        description="ID of the exchange associated with the portfolio"
    )
    base_currency_id: Optional[UUID] = Field(
        description="ID of the base currency of the portfolio"
    )
    created_at: datetime | None = Field(
        default_factory=datetime.now,
        description="Timestamp of when the portfolio was created",
    )
    updated_at: datetime | None = Field(
        default_factory=datetime.now,
        description="Timestamp of when the portfolio was last updated",
    )
    balance: float = Field(
        default=0.0, description="The total balance of the portfolio"
    )


class Position(BaseModel):
    id: Optional[UUID] = Field(None, description="Unique identifier of the position")
    portfolio_id: UUID = Field(description="ID of the associated portfolio")
    asset_id: UUID = Field(description="ID of the associated asset")
    quantity: float = Field(
        description="Quantity of the asset held in the position", alias="amount"
    )
    average_price: float = Field(
        alias="value", description="Average price of the asset in the position"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: pendulum.now("UTC"),
        description="Timestamp of when the position was created",
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: pendulum.now("UTC"),
        description="Timestamp of when the position was last updated",
    )
    status: PositionStatus = PositionStatus.OPEN
    opened_at: datetime | None = Field(
        datetime.now(), description="The datetime the position was opened."
    )
    closed_at: datetime | None = Field(
        None, description="The datetime the position was closed."
    )
    opened_trade: uuid.UUID | None = Field(
        None, description="The trade_id of the trade that opened this position."
    )
    closed_trade: uuid.UUID | None = Field(
        None,
        description="The trade_id of the trade that closed this trade. Used for fast look-ups.",
    )
