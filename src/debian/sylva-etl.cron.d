*/5 * * * *  sylva   flock -n /var/lock/sylva-etl-store -c "sylva-store" 1>> /var/log/sylva-etl/sylva-store.log 2>> /var/log/sylva-etl/sylva-store-error.log
