import os
import enum

# Gender Enum
class Gender(enum.Enum):
  male = 'Male'
  female = 'Female'

#boolean
NO = 0
YES = 1
BOOLEAN = {
   NO : 'no',
   YES: 'yes'
}

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/var/tmp', 'instance')


# Model
DESCRIPTION_LEN = 254
EMAIL_LEN = 254
STRING_LEN = 64
ZIPCODE_LEN = 6
PW_STRING_LEN = 255
FILE_NAME_LEN = 128
