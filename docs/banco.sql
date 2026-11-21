create extension if not exists vector;

create table if not exists public.documentos_lumina (
    id bigint generated always as identity primary key,
    titulo text not null,
    conteudo text not null,
    embedding vector(384) not null,
    criado_em timestamptz not null default now(),
    constraint documentos_lumina_unico unique (titulo, conteudo)
);

create or replace function public.buscar_documentos_lumina(
    query_embedding vector(384),
    match_count integer default 4,
    match_threshold float default 0.30
)
returns table (id bigint, titulo text, conteudo text, similaridade float)
language sql stable
set search_path = public
as $$
    select d.id, d.titulo, d.conteudo,
           (1 - (d.embedding <=> query_embedding))::float as similaridade
    from public.documentos_lumina d
    where 1 - (d.embedding <=> query_embedding) >= match_threshold
    order by d.embedding <=> query_embedding
    limit least(greatest(match_count, 1), 10);
$$;

alter table public.documentos_lumina enable row level security;
revoke all on public.documentos_lumina from anon, authenticated;
revoke all on function public.buscar_documentos_lumina(vector, integer, float) from public, anon, authenticated;
-- A aplicação utiliza uma chave de servidor (service_role), nunca exposta no navegador.
