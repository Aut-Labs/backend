select max(block_id)
from public.moralis_scan_checkpoints 
    where 
        interaction_hash = '%s' and 
        eth_address = '%s';

select max(block_id), interaction_hash, eth_address
from public.moralis_scan_checkpoints
group by interaction_hash, eth_address;
