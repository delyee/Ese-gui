/*
all of them         все строки внутри правила
any of them         любая строка в правиле
all of ($a*)        все строки чей идентификатор начинается с $a
any of ($a,$b,$c)   любая из $a,$b или $c
1 of ($*)           то же самое что "any of them"
*/

rule {rulename}: tag
{{
    meta:
        description = ""
        author = "delyee"
        date = "{date}"
        sha256sum = "{sha256sum}"
    strings:
        {strings[0]}
        {strings[1]}
        {strings[2]}
    condition:
        all of them
}}
