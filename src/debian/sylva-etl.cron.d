*/7 * * * *  sylva   flock -n /var/lock/sylva-etl -c "sylva-store" 1>> /var/log/sylva-etl/sylva-store.log 2>> /var/log/sylva-etl/sylva-store-error.log
*/13 * * * *  sylva   flock -n /var/lock/sylva-etl -c "sylva-archive" 1>> /var/log/sylva-etl/sylva-archive.log 2>> /var/log/sylva-etl/sylva-archive-error.log
0 3 * * *  sylva   flock -n /var/lock/sylva-etl -c "sylva-clean" 1>> /var/log/sylva-etl/sylva-clean.log 2>> /var/log/sylva-etl/sylva-clean-error.log
