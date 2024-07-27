#
#    foo         = name of the variable
#    type        = type of variable
#    isArr       = boolean
#    isOptional  = boolean : is the variable optional in constructor
#    default     = "default values" | "" |
######
#    constraints = "Primary Key  Unique  Not Null Auto_Increment"
#    map         = "ManyToMany | OneToMany | OneToOne "  | ""
#    mappedBy    = variable name that you want to map
#    fetchType   = lazy | eager
{
    "variables":[
        #don't remove the id field because it serve as a primary key for database.
        {
            "name":"id",
            "type":"long",
            "isArr":False,
            "default":"",
            "constraints":"Primary Key not null",
            "map":"",
            "mappedBy":"",
            "fetchType":"",
        },
        {
            "name":"createdDateTime",
            "type":"datetime",
            "isArr":False,
            "default":"",
            "constraints":"not null",
            "map":"",
            "mappedBy":"",,
            "fetchType":"",
        },
    ]

    }
