# instacerty!

This Package enables the instant generation of certificates in PDF format, offering customizable fields such as name, course, instructor, and more. It supports optional elements like background images, badges, signatures, certificate numbers, and issue dates, providing flexibility for users to personalize certificates quickly and efficiently. Ideal for educational institutions, training programs, or events, it simplifies the creation of professional certificates. Future updates will introduce more features such as custom fonts, date format, dynamic QR codes, and enhanced design templates to further enrich the certificate creation process
## Output
![Logo](https://raw.githubusercontent.com/iammadhanraj/mystaticfiles/main/InstaCerty/Sample_Certificate.png)

##  Features
### 1. Generate Certificates
- **Input Fields:** Allows users to input the name, course, instructor, and other details.
- **Dynamic PDF Generation:** Automatically generates certificates in both PDF using the provided information.
- **Customizable Layout:** The certificates are designed in A4 landscape format with a user-defined background watermark or logo and signature also.
### 2. QR Code Integration
- A QR code is automatically generated and added to the bottom of the certificate.
- The QR code encodes information such as the certificate number,name, course like allowing for quick verification.
### 3. File Handling
- **Generate & Store:** The application stores the generated certificates (PDF) in the current directory when you create **.py** file and using this **Package** 
### 4. Download Certificates
- Certificates in PDF from automatically download after **Generate Processs** Complete.
### 5. Date Formatting
- The application formats dates in the day-month-year format for consistency on certificates(in future it will be Customizable format).

## Installation

1.Clone the repository:

```bash
pip install instacerty
```

2.Import:

```pyhon
from instacerty import generate_certificate
```




## Usage
### 1. Basic Usage

```python
from instacerty import generate_certificate

# Certificate details(this 3 field is mandatory)
name = "Alita"
course = "Python Programming"
instructor = "Youtube"

# Generate the certificate
generate_certificate(
    name=name,
    course=course,
    instructor=instructor
)

```

### Output
![Logo](https://raw.githubusercontent.com/iammadhanraj/mystaticfiles/main/InstaCerty/Sample_Certificate.png)

### 2. Customizable

```python
from instacerty import generate_certificate

# Certificate details
name = "Alita"
course = "Python Programming"
instructor = "Youtube"

#Change custom bg
bg_image_path = "path/to/background.jpg"
#Change custom badge
badge_image_path = "path/to/badge.png"
#Change custom signature
signature_image_path = "path/to/signature.png"
#Where you want to save the PDF Certificates
custom_save_path="certificates/"
#Custom certificate number
custom_certificate_number="CERT123456"
#Custom issue date
custom_issue_date="15-08-2024"

# Generate the certificate
generate_certificate(
    name=name,
    course=course,
    instructor=instructor,
    bg=bg_image_path,
    is_badge=True,
    badge_img=badge_image_path,
    is_signature=True,
    signature_img=signature_image_path,
    save_path=custom_save_path,
    certificate_number=custom_certificate_number,
    issue_date=custom_issue_date
)

```
## Function

### 1 . generate_certificate
- This is main function for generate certificates

#### Parameters
- **name (str):** The name of the individual receiving the certificate.
- **course (str):** The name of the course for which the certificate is awarded.
- **instructor (str):** The name of the instructor issuing the certificate.
- **bg (str, optional):** If you want to use custom background for your certificates, the file path to a background image for the certificate else it will take the default background image. Defaults to None.
- **is_badge (bool, optional):** Whether to include a badge on the certificate. Defaults to True.
- **badge_img (str, optional):** If you want to use custom badge for your certificates the file path to the badge image else it use default badge image. Defaults to None.
- **is_signature (bool, optional):** Whether to include a signature on the certificate. Defaults to True.
- **signature_img (str, optional):** If you want to use custom signature for your certificates The file path to the signature image else it use default signature image. Defaults to None.
- **save_path (str, optional):** The file path where the generated PDF certificates will be saved. Defaults to None.
- **certificate_number (str, optional):** If you want to use custom Certificate Number for your certificates , you can use this Parameter. Defaults to None.
- **issue_date (str, optional):** If you want to use custom **Issue Date** for your certificates , you can use this Parameter . Defaults to None.

### 2 . get_certy_number
- This function for generate unique 12-Digit Alphanumeric Number


## Other Packages
The following **Packages** are dependencies for *instacerty!*
- chardet
- colorama
- pillow
- qrcode
- reportlab
## GitHub
[![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/iammadhanraj/instacerty)
