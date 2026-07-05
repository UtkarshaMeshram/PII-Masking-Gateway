def mask_pii(text, detected):
    
    masked_text = text

    for category in detected:
        for value in detected[category]:

            if category == "email":
                parts = value.split("@")
                masked = parts[0][0] + "***@" + parts[1]

            elif category == "phone":
                masked = value[:2] + "******" + value[-2:]

            elif category == "aadhaar":
                masked = "XXXX XXXX " + value[-4:]
                
            elif category == "cvv":
                masked = "***"

            else:
                masked = "****"

            masked_text = masked_text.replace(value, masked)

    return masked_text