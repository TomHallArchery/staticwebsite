# Encodings

# all
pyftsubset \
  PublicSans-VariableFont_wght.ttf \
  --output-file="PublicSans-VariableFont_wght.woff2" \
  --flavor=woff2 \
  --layout-features=* \
  --unicodes="*" &&

# Latin
  pyftsubset \
    RobotoSlab-VariableFont_wght.ttf \
    --output-file="RobotoSlab-VariableFont_wght-Latin.woff2" \
    --flavor=woff2 \
    --layout-features=* \
    --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"

# English
pyftsubset \
  PublicSans-VariableFont_wght.ttf \
  --output-file="PublicSans-VariableFont_wght-Eng.woff2" \
  --flavor=woff2 \
  --layout-features=* \
  --unicodes="U+0000-00A0,U+00A2-00A9,U+00AC-00AE,U+00B0-00B7,U+00B9-00BA,U+00BC-00BE,U+00D7,U+00F7,U+2000-206F,U+2074,U+20AC,U+2122,U+2190-21BB,U+2212,U+2215,U+F8FF,U+FEFF,U+FFFD"

# Minimal English
pyftsubset \
  PublicSans-VariableFont_wght.ttf \
  --output-file="PublicSans-VariableFont_wght-Min.woff2" \
  --flavor=woff2 \
  --layout-features-="dnom,numr,frac" \
  --unicodes="U+0000-00A0"
