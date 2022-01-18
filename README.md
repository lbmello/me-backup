# me-backup

# Install

Baixar o pacote do PIP.
```shell
    $ sudo python -m pip install me-backup
```

Para testar a instalação, rode o comando de help:
```
    $ sudo python -m me_backup --help   
    Usage: python -m me_backup [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    install  Create needed files (run with sudo).
```

Caso não exista nenhuma instalação anterior em `/etc/me-backup`, simplesmente chame o módulo dentro da instalação de python do sistema usando sudo. Isso irá abrir um formulário para instação dos recursos.

Neste caso, é exigido uso de privilégio, porque o pacote irá realizar alterações na pasta `/etc/me-backup` e no cron do usuário informado na instalação em `/var/spool/cron/`.

```shell
    $ sudo python -m me_backup install
    
    Me-backup never runned, this follow steps will create the tool folder and config file into /etc/me-backup! (need sudo)
    Default User: [lucas] 
    Users shell rc: [/home/lucas/.zshrc]
    Task file: [/etc/me-backup/tasks.yaml] 
    Log path: [/etc/me-backup/mebk.log] 
    Log level: [INFO] 
    Default host: [127.0.0.1]               
    Default crontab path: [/var/spool/lucas]
```

Pronto! Rodando o help novamente, outros comandos para uso serão listados.

```shell
    $ sudo python -m me_backup --help
    
    Usage: python -m me_backup [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    generate_yaml  Create a tasks.yaml model file.
    print_rsync    Return the rsync command
    run_now        Run the backup tasks right now.
    schedule       Schedule the tasks to run using your time configurations.
```

Dentro da pasta `/etc/me-backup` o arquivo `tasks.yaml` será criado. Nele existe uma tarefa de modelo pré-configurada:

```yaml
    tasks:
    - name: backup home
        slug: bkp_home
        src: /home/lucas/Arduino
        remote_src: False
        dst: /mnt/storage/backup/TESTE/dst1/Arduino
        remote_dst: False
        copy_config:
        type: sync
        wake_on_lan:
        enabled: False
        mac_address: 'd8:9c:67:07:87:e3'
        frequency:
        shortcut: daily
        exclude:
        extensions:
            - txt
        folder:
            - .ssh
```