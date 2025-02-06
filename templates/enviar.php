 <?php
  if(isset($_POST['email']) && !empty($_POST['email'])){
$nome = addslashes($_POST['name']); 
$email = addslashes($_POST['email']);
$mensagem = addslashes($_POST['mesage']); 
} 
$to = "vestibulae21@gmail.com";
$subject = "Teste";
$body = "Nome: ".$nome."\r\n"
        ."Email: ".$email."\r\n"
        ."Mensagem: ".$mensagem;
$header = "From:thiagoazevedo912@gmail.com"."\r\n"
            ."Reply-To:".$email."\r\n"
            ."X=Mailer:PHP/".phpversion();
if(mail($to,$subject,$body,$header)){
    echo("Deu bom");
}else{
    echo("Deu ruim");
}
 ?>

