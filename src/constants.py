from .models import *
Models = {
    "RemoveBg":{
        "Class":RemoveBg,
        "Inputs":{"X-Api-Key":{"type":"api","placeholder":"xxxx-xxxx-xxxx-xxxx"},"bg_color":{"type":"string","placeholder":"fff"},"channels":{"type":"string","placeholder":"Request either the finalized image ('rgba', default) or an alpha mask ('alpha')"},"size":{"type":"string","placeholder":"full/preview"},"type":{"type":"string","placeholder":"auto/car/person"},"bg_image_url":{"type":"string","placeholder":"url"},"roi":{"type":"string","placeholder":"Region of interest"},"format":{"type":"string","placeholder":"Result image format"},"type_level":{"type":"string","placeholder":"Classification level of the detected foreground type"},"crop":{"type":"boolean","default":False},"crop_margin":{"type":"string","placeholder":"Adds a margin around the cropped subject"},"add_shadow":{"type":"boolean","default":False},"semitransparency":{"type":"boolean","default":True}},
        "Link":"https://www.remove.bg/de/api#api-reference",
        "About":"By making complicated tech simple, we strive to enable individuals and businesses of all sizes to benefit from the recent advances in Visual AI. Our tools simplify and accelerate workflows, foster creativity, and enable others to create new products.",
    },
    "PhotoRoom":{
        "Class":PhotoRoom,
        "Inputs":{"x-api-key":{"type":"api","placeholder":"xxxx-xxxx-xxxx-xxxx"},"format":{"type":"string","placeholder":"png/jpg","default":"png"},"channels":{"type":"string","placeholder":"rgba/alpha","default":"rgba"},"bg_color":{"type":"string","placeholder":"green"},"size":{"type":"string","placeholder":"preview/medium/hd/full","default":"full"},"crop":{"type":"string","placeholder":"true/false","default":"false"}},
        "Link":"https://www.photoroom.com/api/docs/reference/b6f599c7c438c-remove-background",
        "About":"PhotoRoom API The power of PhotoRoom, automated. Adjust images, remove, and replace backgrounds in seconds",
    },
    "Clipdrop":{
        "Class":Clipdrop,
        "Inputs":{"x-api-key":{"type":"api","placeholder":"xxxx-xxxx-xxxx-xxxx"}},
        "Link":"https://clipdrop.co/",
        "About":"To remove the background from an image",
    },
    "Slazzer":{
        "Class":Slazzer,
        "Inputs":{"API-KEY":{"type":"api","placeholder":"xxxx-xxxx-xxxx-xxxx"},"bg_image_url":{"type":"string","placeholder":"url"},"bg_color_code":{"type":"string","placeholder":"#72E4B3"},"format":{"type":"string","placeholder":"png/jpg"},"crop":{"type":"boolean","default":False},"crop_margin":{"type":"string","placeholder":"Adds a margin around the cropped subject"},"scale":{"type":"string","placeholder":"This parameter scales the subject in the output image"},"position":{"type":"string","placeholder":"This parameter place the subject within the image canvas"},"preview":{"type":"boolean","default":False},"channel":{"type":"string","placeholder":"This parameter will return the image channel(red, green, blue, alpha) in RGBA or alpha mask format"},"roi":{"type":"string","placeholder":"This parameter when given will let you extract the region of interest of a particular image"}},
        "Link":"https://www.slazzer.com/api",
        "About":"Slazzer is an AI powered tool that uses advanced computer vision algorithms to remove bg from any image online",
    },
    "ClickMajic":{
        "Class":ClickMajic,
        "Inputs":{"api_key":{"type":"api","placeholder":"xxxx-xxxx-xxxx-xxxx"},"bgImageUrl":{"type":"string","placeholder":"url"},"bgColorCode":{"type":"string","placeholder":"#72E4B3"},"format":{"type":"string","placeholder":"png/jpg"},"crop":{"type":"boolean","default":False},"cropMargin":{"type":"string","placeholder":"Adds a margin around the cropped subject"},"scale":{"type":"string","placeholder":"This parameter scales the subject in the output image"},"position":{"type":"string","placeholder":"This parameter place the subject within the image canvas"},"preview":{"type":"boolean","default":False},"channel":{"type":"string","placeholder":"This parameter will return the image channel(red, green, blue, alpha) in RGBA or alpha mask format"},"roi":{"type":"string","placeholder":"This parameter when given will let you extract the region of interest of a particular image"}},
        "Link":"https://clickmajic.com/api",
        "About":"Clickmajic is photo background remover software that lets you easily remove backgrounds from photos",
    },
    "NoApi":{
        "Class": NoApi,
        "Inputs":{"Url":{"type":"url","placeholder":"https://www.domain.*/api/"}},
        "Link":"https://www.github.com/qwersyk",
        "About":"None",
    },

}
