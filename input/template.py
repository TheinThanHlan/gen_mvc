#
#    foo         = name of the variable
#    type        = type of variable
#    isArr       = boolean
#    isOptional  = boolean : is the variable optional in constructor
#    default     = "default values" | "" |
#    constraints = "PrimaryKey  Unique  NotNull AutoIncrement"
#    map         = "ManyToMany | OneToMany | OneToOne "  | ""
#    mappedBy    = variable name that you want to map
{
    "variables":[
        {
            "name":"id",
            "type":"long",
            "isArr":False,
            "isOptional":True,
            "default":"",
            "constraints":"primary_key",
            "map":"",

        },
        {
            "name":"createdDateTime",
            "type":"datetime",
            "isArr":False,
            "isOptional":True,
            "default":""
            "constraints":"not_null"
            "map":"",
        },
    ]

    }
