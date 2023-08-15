use axum::{routing::get, Router};
use clap::Parser;
use std::net::SocketAddr;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

mod handlers;

#[tokio::main]
async fn main() {
    #[derive(Parser)]
    struct Args {
        #[arg(long, default_value = "127.0.0.1:8080")]
        addr: String,

        #[arg(long)]
        configs: Vec<String>,
    }

    #[derive(OpenApi)]
    #[openapi(
        paths(
            handlers::info::get_info,
        ),
        components(
            schemas(
                handlers::info::Info,
            ),
        ),
        tags(
            (name = "info"),
        ),
    )]
    struct ApiDoc;

    let args = Args::parse();

    let _settings = args.configs.iter()
        .fold(
            config::Config::builder(),
            |b, c| b.add_source(config::File::with_name(c)))
        .build()
        .unwrap();

    let app = Router::new()
        .merge(SwaggerUi::new("/ui").url("/openapi.json", ApiDoc::openapi()))
        .route("/info", get(handlers::info::get_info));

    let addr = args.addr.parse::<SocketAddr>().unwrap();

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
