from pydantic import BaseModel , Field
from typing import Optional
class Candidate(BaseModel):
    brand: Optional[str] = Field(default=None, description="brand name inside the receipt")
    total_cost: Optional[str] = Field(default=None, description="total cost inside the receipt.")
    location: Optional[str] = Field(default=None, description="purchase location of the receipt.")
    purchase_category: Optional[str] = Field(default=None, description="category of the products purchased.")
    brand_category: Optional[str] = Field(default=None, description="""INSERT BRAND CATEGORY FROM THE RECEIPT OCR TEXT. CHOOSE CLOSEST BRAND CATEGORY BASED ON THE OCR FROM THIS ARRAY ["Fashion and Apparel","Jewelry and Watches","Beauty and Personal Care","Automobiles","Real Estate","Travel and Leisure","Culinary Services","Home and Lifestyle","Technology and Electronics","Sports and Leisure","Art and Collectibles","Health and Wellness","Stationery and Writing Instruments","Children and Baby","Pet Accessories","Financial Services","Airline Services","Accommodation Services","Beverages Services","Services"] ELSE IF NOT PRESENT RETURN null""")
    Date: Optional[str] = Field(default=None, description="date from the receipt.")
    currency: Optional[str] = Field(default=None, description="currency used to pay.")
    filename: Optional[str] = Field(default=None, description="generating a file name based on rececipt content.")
    payment_method: Optional[str] = Field(default=None, description="payment method.")
    metadata:Optional[str] = Field(default=None, description="metadata for travel and insurance recceipts. ")