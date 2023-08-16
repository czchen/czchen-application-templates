use std::collections::HashMap;
use std::io::Read;

use testcontainers::clients::Cli;
use testcontainers::core::WaitFor;
use testcontainers::Image;

struct Postgres {
    name: String,
    tag: String,
    env_vars: HashMap<String, String>,
}

impl Postgres {
    fn new(name: String, tag: String) -> Self {
        let mut env_vars = HashMap::new();

        env_vars.insert("POSTGRES_DB".to_owned(), "postgres".to_owned());
        env_vars.insert("POSTGRES_HOST_AUTH_METHOD".into(), "trust".into());

        Self {
            name,
            tag,
            env_vars,
        }
    }
}

impl Image for Postgres {
    type Args = ();
    fn name(&self) -> String {
        self.name.clone()
    }
    fn tag(&self) -> String {
        self.tag.clone()
    }
    fn ready_conditions(&self) -> Vec<WaitFor> {
        vec![WaitFor::message_on_stderr(
            "database system is ready to accept connections",
        )]
    }
    fn env_vars(&self) -> Box<dyn Iterator<Item = (&String, &String)> + '_> {
        Box::new(self.env_vars.iter())
    }
}

fn main() {
    let podman = Cli::podman();
    let image = Postgres::new("docker.io/postgres".to_owned(), "15.4-bookworm".to_owned());

    podman.run(image);

    println!("Press any key to stop...");
    let buffer = &mut [0u8];
    std::io::stdin().read_exact(buffer).unwrap();
}
