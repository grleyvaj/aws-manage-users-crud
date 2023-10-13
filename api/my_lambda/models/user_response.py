from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    last_name: str
    charge: str
    type: str
    status: str
    tenant_id: str
    token_invite: str
    created_at: str

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "charge": self.charge,
            "type": self.type,
            "status": self.status,
            "tenant_id": self.tenant_id,
            "token_invite": self.token_invite,
            "created_at": self.created_at,
        }