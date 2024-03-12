create view max_blocks as 
    select max(blockid), chainid, txto, txfrom 
    from public.tx_fetched 
    group by chainid, txfrom, txto
with cascaded check option;

