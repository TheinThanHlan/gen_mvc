#
#    foo         = name of the variable
#    type        = type of variable
#    isArr       = boolean
#    isOptional  = boolean : is the variable optional in constructor
#    default     = "default value of class" | "" 
######
#    constraints = "Primary Key  Unique  Not Null Auto_Increment"
#    map         = "ManyToMany | OneToMany | OneToOne "  | ""
#    mappedBy    = variable name that you want to map
#    fetchType   = lazy | eager
#
#
#
#
{
    "variables":[
        
        #don't remove the id field because it serve as a primary key for database. 
        #dont change the type it will certainly lead to some error 🫠
        {
            "name":"id",
            "type":"long",
            "isArr":False,
            "isOptional":True,
            "default":"0",
            "constraints":"Primary Key not null",
            "map":"",
            "mappedBy":"",
            "fetchType":"",
        },


        #you can remove or change name do as you like this field
        {
            "name":"createdDateTime",
            "type":"datetime",
            "isOptional":True,
            "isArr":False,
            "default":"",
            "constraints":"not null",
            "map":"",
            "mappedBy":"",
            "fetchType":"",
        },

    ]

    }
